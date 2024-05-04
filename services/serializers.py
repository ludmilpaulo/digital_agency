from rest_framework import serializers
from .models import Service, ServiceCategory, ServiceRequest

from django.contrib.auth import get_user_model
User = get_user_model()

class ServiceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Service
        fields = '__all__'

   
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'



class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['service', 'user', 'message', 'phone', 'address', 'email']

    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())