from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home, register, profile, logout_view, edit_profile,
                    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView)

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create-alt'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update-alt'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete-alt'),
]