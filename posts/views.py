from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Post, Comment
from .serializers import CommentSerializer, PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializer




class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        This method filters the comments by the post ID passed in the URL.
        """
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        """
        This method sets the post for a new comment based on the post ID.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(post=post)