from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, AccessMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post, PostCategory, Author, Comment
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import *
from .filters import *
from .tasks import *


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'endex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        return redirect('/')


class AuthorList(ListView):
    model = Author
    ordering = '-user'
    template_name = 'users/authors.html'
    context_object_name = 'Author'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'users/author.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Author.objects.get(pk=self.kwargs['pk']).post_set.all().order_by('-id')
        return context


class PostList(ListView):
    model = Post
    ordering = 'titles'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post_id'

    # Представление для просмотра конкретного объявления
    def post_detail_view(request, pk):
        template_name = 'post/post_detail.html'
        # получаем текущее объявление
        posts_id = get_object_or_404(Post, id=pk)
        # список всех принятых откликов на это объявление
        comment = posts_id.comment.filter()
        new_comment = None
        if request.method == 'POST':
            # Отклик оставлен
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # создаем объект отлика, но пока не сохраняем в БД
                new_comment = comment_form.save(commit=False)
                # привязываем отклик к текущему объявлению
                new_comment.posts = posts_id
                new_comment.user = request.user
                # сохраняем отклик в БД
                new_comment.save()
                # отправляем уведомление автору о новом отклике на его объявление
                post_comment_notification.delay(new_comment.pk)
        else:
            comment_form = CommentForm()

        context = {
            'post_id': posts_id,
            'comment': comment,
            'new_comment': new_comment,
            'comment_form': comment_form
        }

        return render(request, template_name, context)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    permission_required = ('posts.update_post',)
    form_class = PostForm
    success_url = '/posts'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = 'posts'
        return super().form_valid(form)


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_update.html'
    permission_required = ('posts.create_post',)
    form_class = PostForm
    success_url = '/posts'

    def form_valid(self, form):
        author = User.objects.get(id=self.request.user.id)
        post = form.save(commit=False)
        post.author = author
        # вызываем метод super, чтобы у объявления появился pk
        result = super().form_valid(form)
        # уведомляем подписчиков о новом объявлении в их любимой категории
        posts_add_notification.delay(post.pk)
        return result


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    permission_required = ('posts.post_delete',)
    form_class = PostForm
    success_url = '/posts'


class CategoryList(ListView):
    model = Category
    template_name = 'posts/categories.html'
    context_object_name = 'categories'


class PostCategory(ListView):
    model = Post
    ordering = '-id'
    template_name = 'post/postes.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.queryset = Category.objects.get(pk=self.kwargs['pk']).PostCategory.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in Category.objects.get(pk=self.kwargs['pk']).\
            subscribers.all()
        context['category'] = self.queryset
        return context


class CommentList(ListView):
    model = Comment
    template_name = 'posts/comment.html'
    context_object_name = 'comment'
    paginate_by = 10
    permission_required = ('ads.view_advertisement',)
    raise_exception = True

    # Переопределяем функцию получения списка откликов
    def get_queryset(self):
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = CommentFilter(self.request.GET,
                                       queryset.filter(comment__author_comment=self.request.user),
                                     request=self.request)
        # Возвращаем из функции отфильтрованный список откликов
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset

        return context


class CommentDeleteView(PermissionRequiredMixin, AccessMixin, DeleteView):
    form_class = CommentDeleteForm
    model = Comment
    template_name = 'posts/post_delete.html'
    # требование права на удаление отклика
    permission_required = ('posts.delete_comment',)
    raise_exception = True
    success_url = reverse_lazy('comment')


# Представление, принимающее отклик
@permission_required('ads.change_reply', raise_exception=True)
def comment_approve_view(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.approved = True
    comment.save()
    comment_approve_notification.delay(comment.pk)

    return redirect('/posts/comment/')


@permission_required('posts.change_category', raise_exception=True)
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    data = {'category': category}
    return render(request, 'post/subscribe.html', context=data)


# Представление для отписки от выбранной категории
@permission_required('posts.change_category', raise_exception=True)
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    data = {'category': category}
    return render(request, 'post/unsubscribe.html', context=data)
