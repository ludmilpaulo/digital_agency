from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, CommentViewSet, AuthorViewSet,
    CategoryViewSet, NewsletterSubscriberViewSet,
    approve_comment, reject_comment,
)

router = DefaultRouter()
#router.register(r'posts', PostViewSet)
router.register(r'blogs', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'newsletter', NewsletterSubscriberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comments/<int:pk>/approve/', approve_comment),
    path('comments/<int:pk>/reject/', reject_comment),
]
