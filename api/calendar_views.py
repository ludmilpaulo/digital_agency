# tasks/views.py

from django.conf import settings
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .models import GoogleCredentials

import os

GOOGLE_CLIENT_ID = getattr(settings, "GOOGLE_CLIENT_ID", "your-client-id.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = getattr(settings, "GOOGLE_CLIENT_SECRET", "your-client-secret")
GOOGLE_REDIRECT_URI = getattr(
    settings,
    "GOOGLE_REDIRECT_URI",
    "https://www.maindodigital.com/api/google/oauth2callback/",
)
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/calendar"]

def creds_to_dict(creds):
    return {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def google_auth_start(request):
    # Build the Google OAuth2 flow
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',  # Ensures refresh token is always returned
    )
    request.session['oauth_state'] = state
    return Response({"url": authorization_url})

@api_view(["GET"])
@permission_classes([AllowAny])
def google_auth_callback(request):
    # Handles Google redirect after user grants access
    state = request.session.get('oauth_state')
    if not state:
        return Response({"error": "Session expired. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=GOOGLE_SCOPES,
        state=state,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    try:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
    except Exception as e:
        return Response({"error": f"Failed to fetch token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    creds = flow.credentials

    # Save credentials for the user (you may want to implement proper user linking here)
    user = request.user if request.user.is_authenticated else None
    if not user:
        return Response({"error": "User not authenticated!"}, status=status.HTTP_403_FORBIDDEN)
    GoogleCredentials.objects.update_or_create(
        user=user,
        defaults={"credentials": creds_to_dict(creds)},
    )
    return Response({"success": True, "msg": "Google Calendar connected!"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_task_to_calendar(request):
    user = request.user
    try:
        gc = GoogleCredentials.objects.get(user=user)
    except GoogleCredentials.DoesNotExist:
        return Response({"error": "No Google credentials found"}, status=400)

    creds = Credentials(**gc.credentials)
    service = build('calendar', 'v3', credentials=creds)

    # Get task info from POST data
    title = request.data.get("title")
    description = request.data.get("description", "")
    start_date = request.data.get("start_date")  # "YYYY-MM-DD"
    due_date = request.data.get("due_date")      # "YYYY-MM-DD"
    if not (title and start_date and due_date):
        return Response({"error": "Missing required fields"}, status=400)

    event = {
        "summary": title,
        "description": description,
        "start": {"date": start_date},
        "end": {"date": due_date},
    }
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
    except Exception as e:
        return Response({"error": f"Google Calendar API error: {str(e)}"}, status=400)
    return Response({"event_id": event["id"], "htmlLink": event.get("htmlLink")})

