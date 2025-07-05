# services/urls.py
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, PlanViewSet

router = DefaultRouter()
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"plans", PlanViewSet, basename="plan")

urlpatterns = router.urls
