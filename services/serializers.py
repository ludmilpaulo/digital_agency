from rest_framework import serializers
from .models import Service, ServiceCategory, ServiceRequest

class ServiceSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_image_urls(self, obj):
        if obj.images.exists():
            # Get the request object from context
            request = self.context.get('request')
            if request is not None:
                # Build and return absolute URLs for all images associated with the product
                return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        return None

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'



class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'