from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@csrf_exempt  # You can remove this if you use JWT/auth headers instead!
def check_staff_view(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        user_id = body.get("user_id")
        if not user_id:
            return JsonResponse({"detail": "user_id is required"}, status=400)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"detail": "User not found"}, status=404)

        return JsonResponse({"is_staff": user.is_staff})
    except Exception as e:
        return JsonResponse({"detail": f"Error: {str(e)}"}, status=400)
