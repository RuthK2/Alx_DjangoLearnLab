from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post CRUD operations with filtering and pagination."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
   
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['author', 'created_at']  # exact matching
    ordering_fields = ['created_at', 'updated_at', 'title']  # ordering
    search_fields = ['title', 'content']  # search by keyword
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return Post.objects.filter(author=self.request.user)
        return Post.objects.all()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ['post', 'author']  # exact matching
    ordering_fields = ['created_at', 'updated_at']  # ordering
    search_fields = ['content']  # search by keyword
     
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return Comment.objects.filter(author=self.request.user)
        return Comment.objects.all()
    
class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.none()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.all()
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')    
