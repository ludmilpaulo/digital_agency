from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer




@api_view(['POST'])
def post_comments(request, post_id):
    """
    Create a new comment for a post.
    """
    post = get_object_or_404(Post, pk=post_id)
    # Update serializer to only include comment-related fields
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post)  # Automatically links the comment to the fetched post
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(APIView):
    def get(self, request, post_id):
        comments = Comment.objects.filter(post__id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)