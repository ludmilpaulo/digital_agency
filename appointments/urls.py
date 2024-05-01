from django.urls import path
from .views import AppointmentListCreateAPIView, AppointmentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('appointments/', AppointmentListCreateAPIView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentRetrieveUpdateDestroyAPIView.as_view(), name='appointment-detail'),
]
