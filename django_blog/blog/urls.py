from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home, register, profile, logout_view, edit_profile,
                    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
                    CommentCreateView, CommentUpdateView, CommentDeleteView, search_posts, PostByTagListView)

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
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', search_posts, name='search'),
    path('tags/<str:tag_name>/', PostByTagListView.as_view(), name='posts-by-tag'),
]