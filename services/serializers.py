from rest_framework import serializers
from .models import Service, Plan
from .models import ProposalRequest

class ProposalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalRequest
        fields = "__all__"  

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'features', 'cta', 'popular', 'order']

class ServiceSerializer(serializers.ModelSerializer):
    plans = PlanSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = ['id', 'title', 'slug', 'description', 'icon', 'featured', 'order', 'plans']
