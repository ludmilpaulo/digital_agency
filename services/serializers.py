from rest_framework import serializers
from .models import Service, ServiceCategory, ServiceRequest

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
        fields = '__all__'