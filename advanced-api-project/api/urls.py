from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookDetail, BookCreate, BookUpdate, BookDelete

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('books/create/', BookCreate.as_view(), name='book-create'),
    path('books/update/', BookUpdate.as_view(), name='book-update-no-id'),
    path('books/delete/', BookDelete.as_view(), name='book-delete-no-id'),
    path('books/<int:pk>/update/', BookUpdate.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDelete.as_view(), name='book-delete'),
]
