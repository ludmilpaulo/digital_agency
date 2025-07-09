from rest_framework import viewsets
from .models import  Card
from .serializers import CardSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(assignees__id=user_id).distinct()  # <--- FIXED
        return queryset
