from .import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register(r'notifications', views.NotificationViewSet, basename='notifications')
urlpatterns = routers.urls

