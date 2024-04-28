from django.urls import path
from .views import ServiceListCreateAPIView, ServiceRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('services/', ServiceListCreateAPIView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyAPIView.as_view(), name='service-detail'),
]
