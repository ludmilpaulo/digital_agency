from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Board, List, Card
from .serializers import BoardSerializer, ListSerializer, CardSerializer

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(users=self.request.user)

    def perform_create(self, serializer):
        board_instance = serializer.save()
        board_instance.users.add(self.request.user)

class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return List.objects.filter(board__users=self.request.user)

    def perform_create(self, serializer):
        list_instance = serializer.validated_data['board']
        if self.request.user in list_instance.users.all():
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to create a list on this board.")

class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(list__board__users=self.request.user)

    def perform_create(self, serializer):
        card_instance = serializer.validated_data['list']
        if self.request.user in card_instance.board.users.all():
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to create a card in this list.")
