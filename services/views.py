# services/views.py
from rest_framework import viewsets
from .models import Service, Plan
from .serializers import ServiceSerializer, PlanSerializer

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all().order_by("order")
    serializer_class = ServiceSerializer

class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.all().order_by("order")
    serializer_class = PlanSerializer
