from django.urls import path
from .views import create_appointment

urlpatterns = [
    path('appointments/', create_appointment, name='create_appointment'),
]
