# views.py
from rest_framework import viewsets
from .models import Board, List, Card
from .serializers import BoardSerializer, ListSerializer, CardSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

User = get_user_model()

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production!

    def perform_create(self, serializer):
        board = serializer.save()
        managers = list(serializer.validated_data.get('managers', []))
        # Always add the requesting user as manager (if authenticated)
        if self.request.user.is_authenticated and self.request.user not in managers:
            board.managers.add(self.request.user)
        for user in managers:
            board.managers.add(user)
        board.save()


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        queryset = super().get_queryset().prefetch_related('cards')
        if user_id:
            # Only lists with at least one card assigned to user
            queryset = queryset.filter(cards__assignees__id=user_id).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        # You may want to optimize serialization: prefetch cards and their assignees
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(assignees__id=user_id)
        return queryset.distinct()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'Completed':
            return Response(
                {"detail": "Cannot delete a completed card."},
                status=400,
            )
        return super().destroy(request, *args, **kwargs)


# Optionally, user list for assignment dropdowns
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
