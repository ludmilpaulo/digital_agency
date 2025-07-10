from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@csrf_exempt  # Remove this if you use authentication (like JWT)
def check_staff_view(request):
    print("Step 1: Received request")  # STEP 1

    if request.method != "POST":
        print("Step 2: Method not allowed (received {})".format(request.method))
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        print("Step 3: Attempting to parse JSON body")
        body_unicode = request.body.decode("utf-8")
        print("Raw body:", body_unicode)
        body = json.loads(body_unicode)
        user_id = body.get("user_id")
        print("Step 4: Extracted user_id:", user_id)

        if not user_id:
            print("Step 5: No user_id provided")
            return JsonResponse({"detail": "user_id is required"}, status=400)

        print("Step 6: Attempting to retrieve user with id:", user_id)
        try:
            user = User.objects.get(id=user_id)
            print("Step 7: User found:", user)
        except User.DoesNotExist:
            print("Step 7: User not found for id:", user_id)
            return JsonResponse({"detail": "User not found"}, status=404)

        print("Step 8: Returning is_staff:", user.is_staff)
        return JsonResponse({"is_staff": user.is_staff})
    except Exception as e:
        print("Step 9: Exception occurred:", str(e))
        return JsonResponse({"detail": f"Error: {str(e)}"}, status=400)
