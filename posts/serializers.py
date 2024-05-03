from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Post, Comment



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        post_id = self.context['view'].kwargs.get('post_id')
        validated_data['post'] = get_object_or_404(Post, pk=post_id)
        return super().create(validated_data)

        
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'published_date', 'comments']

