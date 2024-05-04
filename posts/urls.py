from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentListView, PostViewSet, post_comments

router = DefaultRouter()
router.register(r'blogs', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', post_comments, name='post-comments'),
    path('blog/<int:post_id>/comments/', CommentListView.as_view(), name='post-comments'),
]
