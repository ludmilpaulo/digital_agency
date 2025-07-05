from rest_framework import viewsets, permissions, generics, status
from .models import Post, Author, Comment, Category, Tag, NewsletterSubscriber
from .serializers import (
    PostSerializer, AuthorSerializer, CommentSerializer,
    CategorySerializer, TagSerializer, NewsletterSubscriberSerializer
)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author', 'category').prefetch_related('tags', 'comments')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        post = self.get_object()
        related = Post.objects.filter(category=post.category).exclude(pk=post.pk)[:4]
        return Response(PostSerializer(related, many=True).data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        trending = Post.objects.order_by('-views')[:5]
        return Response(PostSerializer(trending, many=True).data)

    @action(detail=False, methods=['get'])
    def tags(self, request):
        tags = Tag.objects.all()
        return Response(TagSerializer(tags, many=True).data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)  # Assumes logged-in authors

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        # Default: not approved, unless admin
        serializer.save(is_approved=self.request.user.is_staff if self.request.user.is_authenticated else False)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class NewsletterSubscriberViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']

# Extra: Approve/Reject comments (admin only)
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def approve_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.is_approved = True
    comment.save()
    return Response({'status': 'approved'})

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def reject_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return Response({'status': 'rejected'})
