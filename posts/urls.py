# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

# The key step is to ensure the paths below are included
urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='post-comments'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'update',
        'delete': 'destroy'
    }), name='post-comment-detail'),
]
