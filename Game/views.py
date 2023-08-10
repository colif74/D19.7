from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post, PostCategory, Author, Comment
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import *
from .filters import *



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'endex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


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
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

#
# # Представление для просмотра конкретного объявления
# def ad_detail_view(request, pk):
#     template_name = 'ads/ad_detail.html'
#     # получаем текущее объявление
#     adv = get_object_or_404(Post, id=pk)
#     # список всех принятых откликов на это объявление
#     replies = adv.replies.filter(approved=True)
#     new_reply = None
#     if request.method == 'POST':
#         # Отклик оставлен
#         reply_form = CommentForm(data=request.POST)
#         if reply_form.is_valid():
#             # создаем объект отлика, но пока не сохраняем в БД
#             new_reply = reply_form.save(commit=False)
#             # привязываем отклик к текущему объявлению
#             new_reply.adv = adv
#             new_reply.user = request.user
#             # сохраняем отклик в БД
#             new_reply.save()
#             # отправляем уведомление автору о новом отклике на его объявление
#             comment_add_notification.delay(new_reply.pk)
#     else:
#         reply_form = CommentForm()
#
#     context = {
#         'adv': adv,
#         'replies': replies,
#         'new_reply': new_reply,
#         'reply_form': reply_form
#     }
#
#     return render(request, template_name, context)
#

class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post_id'


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
        post = form.save(commit=False)
        post.category = 'posts'
        return super().form_valid(form)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    permission_required = ('posts.post_delete',)
    form_class = PostForm
    success_url = '/posts'


class CommentList(ListView):
    model = Comment
    template_name = 'posts/comment.html'
    context_object_name = 'comment'

