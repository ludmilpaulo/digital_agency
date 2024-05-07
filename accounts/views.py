
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.parsers import *
from rest_framework.decorators import *


from django.core.mail import send_mail

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
import json

from django.contrib.auth import get_user_model
User = get_user_model()




@api_view(['POST'])
def custom_signup(request, format=None):
    print("Received data:", request.data)
    if request.method == 'POST':
        try:
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")

            print("Validating inputs...")
            if not username or not email or not password:
                print("Validation error: Missing fields")
                return JsonResponse({"error": "All fields are required"}, status=400)

            print("Checking for existing username and email...")
            if User.objects.filter(username=username).exists():
                print("Validation error: Username exists")
                return JsonResponse({"error": "Username already exists"}, status=400)
            if User.objects.filter(email=email).exists():
                print("Validation error: Email registered")
                return JsonResponse({"error": "Email already registered"}, status=400)

            print("Creating user...")
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            print("Creating token...")
            token, _ = Token.objects.get_or_create(user=user)

            print("Sending email...")
            send_mail(
                subject="Welcome to Maindo Digital Agency",
                message=f"Hello {username},\n\nWelcome to Maindo Digital Agency! We are thrilled to have you with us. Explore our platform and don't hesitate to reach out if you have any questions.\n\nBest,\nMaindo Digital Agency Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            print("Signup successful")
            return JsonResponse({
                "message": "Signup successful",
                "token": token.key,
                "user_id": user.pk,
                "username": user.username
            }, status=201)
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)



@api_view(['POST'])
def custom_login(request, format=None):
    print("Received data:", request.data)
    if request.method == 'POST':
    
        try:
            username_or_email = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
                return JsonResponse({"message": "Login successful",
                                     'token':token.key,
                                        'user_id':user.pk,
                                        'username':user.username,
                                     }, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)
