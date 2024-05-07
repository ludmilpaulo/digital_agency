# app/urls.py
from django.urls import path
from .views import custom_login, custom_signup

urlpatterns = [
    path('custom-login/', custom_login, name='custom-login'),
    path('custom-sign/', custom_signup, name='custom-sign'),
]
