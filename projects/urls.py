from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .submit_project import submit_project_inquiry
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("submit-inquiry/", submit_project_inquiry, name="submit_project_inquiry"),
]
