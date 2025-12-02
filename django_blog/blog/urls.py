from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, register, profile, logout_view, edit_profile

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]