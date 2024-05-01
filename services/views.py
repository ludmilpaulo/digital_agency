from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from django.db.models import Q


from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView


#from django.contrib.auth.models import User
from rest_framework.parsers import *
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import generics
from .models import Service, ServiceCategory, ServiceRequest
from .serializers import ServiceCategorySerializer, ServiceRequestSerializer, ServiceSerializer

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer




class ServiceListCreate(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


@api_view(['DELETE'])
def delete_service(request, pk):
    try:
        # Authenticate the user using the user_id from the request
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id not provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=user_id)

        # Check if the user has permission to delete the product
        service = Service.objects.get(pk=pk)
        if not hasattr(user, 'shop') or user.shop != service.shop:
            return Response({'error': 'User does not have permission to delete this product'}, status=status.HTTP_403_FORBIDDEN)

        # User is authenticated and has permission, delete the product
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Service.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDetailAPIView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRequestCreateAPIView(generics.CreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer