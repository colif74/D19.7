from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import UsersList, PostList, PostDetail, MyLoginView

urlpatterns = [
    path('', ),
    path('login/', MyLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view (next_page='login'), name='logout'),
    path('Users', UsersList.as_view(), name='users'),
    path('Posts', PostList.as_view(), name= 'posts'),
]
