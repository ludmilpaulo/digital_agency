from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Comment, Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']  # Do not include 'post' or 'postId' here

    def create(self, validated_data):
        # 'post' is added in the view, not here
        return Comment.objects.create(**validated_data)