# services/views.py
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from .models import Service, Plan
from .serializers import ServiceSerializer, PlanSerializer

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all().order_by("order")
    serializer_class = ServiceSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]

        # Try by ID
        try:
            return self.get_queryset().get(pk=int(lookup_value))
        except (ValueError, Service.DoesNotExist):
            pass

        # Try by slug
        try:
            return self.get_queryset().get(slug=lookup_value)
        except Service.DoesNotExist:
            raise NotFound("Service not found.")


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.all().order_by("order")
    serializer_class = PlanSerializer
