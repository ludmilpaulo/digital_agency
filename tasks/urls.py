# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.calendar_views import google_auth_callback, google_auth_start

from .task_views import TaskViewSet
from .views import BoardViewSet, ListViewSet, CardViewSet, UserListView

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'lists', ListViewSet, basename='list')
router.register(r'cards', CardViewSet, basename='card')
router.register(r'tasks', TaskViewSet, basename="task")


urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListView.as_view(), name='user-list'),
    path('google/auth/start/', google_auth_start),
    path('google/oauth2callback/', google_auth_callback),
]
