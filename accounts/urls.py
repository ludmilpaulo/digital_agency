# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .group import AllGroupsView, BuiltinGroupViewSet, ProjectGroupViewSet, UserViewSet
from .user_views import UserListView
from .views import custom_login, custom_signup

router = DefaultRouter()
router.register(r'builtin-groups', BuiltinGroupViewSet, basename='builtin-group')
router.register(r'project-groups', ProjectGroupViewSet, basename='project-group')
router.register(r'groups-users', UserViewSet)  # This provides /groups/ etc

urlpatterns = [
    path('groups/all/', AllGroupsView.as_view(), name='all-groups'),
    path('', include(router.urls)),  # <--- THIS LINE IS CRUCIAL
    path('users/', UserListView.as_view(), name='user-list'),
    path('custom-login/', custom_login, name='custom-login'),
    path('custom-sign/', custom_signup, name='custom-sign'),
]
