# tasks/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Board, List, Card

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class CardSerializer(serializers.ModelSerializer):
    assignees = UserSerializer(many=True, read_only=True)
    assignees_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source="assignees", required=False
    )
    class Meta:
        model = Card
        fields = [
            "id", "title", "description", "status", "list",
            "assignees", "assignees_ids", "image", "start_date", "due_date"
        ]

class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    class Meta:
        model = List
        fields = ["id", "name", "board", "cards"]

class BoardSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)
    managers = UserSerializer(many=True, read_only=True)
    users_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source="users", required=False
    )
    managers_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source="managers", required=False
    )
    class Meta:
        model = Board
        fields = [
            "id", "name", "description", "development_link", "repository_link",
            "client_link", "sample_link", "users", "managers", "users_ids", "managers_ids",
            "budget", "budget_used", "deadline", "start_date", "end_date", "status", "lists"
        ]
