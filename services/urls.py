from django.urls import path
from .views import *

urlpatterns = [
   
    path('delete-service/<int:pk>/', delete_service, name='fornecedor-delete-service'),
    path('services_categorias/', ServiceListCreate.as_view(), name='categoria-list-create'),
    
    path('services/', ServiceListAPIView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailAPIView.as_view(), name='service-detail'),
    path('service-requests/', ServiceRequestCreateAPIView.as_view(), name='service-request-create'),
]
