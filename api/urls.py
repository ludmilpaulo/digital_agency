from django.urls import path

from .calendar_views import add_task_to_calendar, google_auth_callback, google_auth_start


urlpatterns = [
    path('google/auth/start/', google_auth_start, name='google_auth_start'),
    path('google/oauth2callback/', google_auth_callback, name='google_auth_callback'),
    path('google/calendar/add/', add_task_to_calendar, name='add_task_to_calendar'),
]
