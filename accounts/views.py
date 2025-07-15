
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
            
            groups = list(user.groups.values_list('name', flat=True))

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
                "username": user.username,
                "groups": groups,
            }, status=201)
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


from django.contrib.auth import authenticate, get_user_model, login
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.http import JsonResponse

@api_view(['POST'])
def custom_login(request, format=None):
    print("------ Login attempt ------")
    print("Raw request data:", request.data)

    if request.method != 'POST':
        print("Method not allowed:", request.method)
        return JsonResponse({"error": "Method not allowed"}, status=405)

    login_id = request.data.get("username") or request.data.get("email")
    password = request.data.get("password")
    print(f"Parsed login_id: {login_id!r}, password present: {bool(password)}")

    if not login_id or not password:
        print("Missing username/email or password!")
        return JsonResponse({"error": "Both username/email and password are required."}, status=400)

    User = get_user_model()
    user = None

    try:
        if '@' in login_id:
            print("Trying to find user by email...")
            user_obj = User.objects.get(email__iexact=login_id)
        else:
            print("Trying to find user by username...")
            user_obj = User.objects.get(username=login_id)
        print(f"User found: {user_obj}")
        # Always use USERNAME_FIELD for authentication
        user = authenticate(request, username=getattr(user_obj, User.USERNAME_FIELD), password=password)
        print("authenticate() result:", user)
    except User.DoesNotExist:
        print("No user with that login_id.")

    if user is not None:
        print("User authenticated! Getting or creating token...")
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        groups = list(user.groups.values_list('name', flat=True))
        print("Groups:", groups)
        print("Returning success response.")
        return JsonResponse({
            "message": "Login successful",
            "token": token.key,
            "user_id": user.pk,
            "username": user.username,
            "email": user.email,
            "groups": groups,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
        }, status=200)

    else:
        print("Login failed: Invalid credentials.")
        return JsonResponse({"error": "Invalid credentials"}, status=400)
