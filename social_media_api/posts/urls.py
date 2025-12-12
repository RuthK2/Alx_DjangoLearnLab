from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()

router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'feed', views.FeedViewSet, basename='feed')

urlpatterns = router.urls + [
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('posts/<int:post_id>/unlike/', views.unlike_post, name='unlike-post'),
]