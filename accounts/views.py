from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Ensuring decoding from bytes to string if needed
            username_or_email = data.get('username')
            password = data.get('password')
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
