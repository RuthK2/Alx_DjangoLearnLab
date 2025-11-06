from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books_class/', views.Booklist.as_view(), name='book_list_class'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]