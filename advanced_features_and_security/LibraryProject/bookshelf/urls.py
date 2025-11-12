from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('book/<int:pk>/', views.book_detail, name='detail'),
    path('book/create/', views.book_create, name='create'),
    path('book/<int:pk>/edit/', views.book_edit, name='edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='delete'),
]