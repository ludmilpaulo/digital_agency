# app/urls.py
from django.urls import path
from .views import custom_login

urlpatterns = [
    path('custom-login/', custom_login, name='custom-login'),
]
