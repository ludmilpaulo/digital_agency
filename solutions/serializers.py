from rest_framework import serializers
from .models import Solution

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'
