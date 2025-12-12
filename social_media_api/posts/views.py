from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from notifications.models import Notification
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


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
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        try:
            user = self.request.user
            following_users = user.following.all()
            return Post.objects.filter(author__in=following_users).order_by('-created_at')
        except AttributeError:
            return Post.objects.none()    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if Like.objects.filter(user=request.user, post=post).exists():
        return Response({'error': 'Post already liked'}, status=status.HTTP_400_BAD_REQUEST)
    
    Like.objects.create(user=request.user, post=post)
    if request.user != post.author:
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(Post)
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target_content_type=content_type,
            target_object_id=post.id
        )
    return Response({'message': 'Post liked'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Like.objects.filter(user=request.user, post=post).delete()
    return Response({'message': 'Post unliked'})
 