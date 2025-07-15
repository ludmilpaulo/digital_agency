# views.py
from rest_framework import viewsets
from .models import Board, List, Card
from .serializers import BoardSerializer, ListSerializer, CardSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q 
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all().prefetch_related("managers", "users")
    serializer_class = BoardSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        manager_id = self.request.query_params.get("manager_id")
        search = self.request.query_params.get("search")

        if user_id:
            qs = qs.filter(Q(users__id=user_id) | Q(managers__id=user_id)).distinct()

        if manager_id:
            qs = qs.filter(managers__id=manager_id).distinct()

        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))

        return qs

    def perform_create(self, serializer):
        board = serializer.save()
        managers = self.request.data.get('managers_ids', [])
        users = self.request.data.get('users_ids', [])
        if self.request.user.is_authenticated:
            board.managers.add(self.request.user)
            board.users.add(self.request.user)
        board.managers.add(*managers)
        board.users.add(*users)
        board.save()

        # --- Send Email Notification ---
        all_users = set(list(board.managers.all()) + list(board.users.all()))
        to_emails = [u.email for u in all_users if u.email]

        if to_emails:
            html_content = render_to_string("email/board_created.html", {
                "board": board,
                "site_name": "Maindo Digital Agency",
                "dashboard_url": "https://www.maindodigital.com/admin",
            })
            send_mail(
                subject=f"[Task Assigned] New Board: {board.name}",
                message=f"You have been assigned to a new board: {board.name}. Please see your dashboard.",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@maindodigital.com"),
                recipient_list=to_emails,
                html_message=html_content,
                fail_silently=True,
            )

    def destroy(self, request, *args, **kwargs):
        board = self.get_object()
        board.delete()
        return Response({"detail": "Board deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




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
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response({"detail": "Card deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Optionally, user list for assignment dropdowns
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
