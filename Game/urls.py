from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from users.views import *

urlpatterns = [

    path('', IndexView.as_view()),
    path('author/', AuthorList.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetail.as_view(), name='author'),
    path('posts/', PostList.as_view(), name= 'posts'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('coder/<str:user>/', CodeRandomView.as_view(), name='coder'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
    path('author/<int:pk>/', AuthorDetail.as_view(), name='author'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='`post_create`'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('comment/', CommentList.as_view(), name='comment'),
    path('category/<int:pk>/subscribers', subscribe, name='subscribers'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('category/', CategoryList.as_view(), name='categories'),
    path('category/<int:pk>/', PostCategory.as_view(), name='posts_of_category_list'),
]

