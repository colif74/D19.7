from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Users, Post
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import PostForm


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class UsersList(ListView):
    model = Users
    ordering = '-user'
    template_name = 'useres/users.html'
    context_object_name = 'users'


class PostList(ListView):
    model = Post
    ordering = '- date_in'
    template_name = 'posts'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post_id'


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/post_update.html'
    permission_required = ('posts.update_post',)
    form_class = PostForm
    success_url = '/posts'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = 'gammer'
        return super().form_valid(form)


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post/post_update.html'
    permission_required = ('posts.create_post',)
    form_class = PostForm
    success_url = '/posts'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = 'gammer'
        return super().form_valid(form)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    permission_required = ('posts.post_delete',)
    form_class = PostForm
    success_url = '/posts'
