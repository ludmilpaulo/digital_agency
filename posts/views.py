from rest_framework import viewsets
from .models import Post, Comment
from .serializers import CommentSerializer, PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializer




class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
