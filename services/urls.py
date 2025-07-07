# services/urls.py
from rest_framework.routers import DefaultRouter

from .proposal_view import ProposalRequestViewSet
from .views import ServiceViewSet, PlanViewSet

router = DefaultRouter()
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"plans", PlanViewSet, basename="plan")
router.register(r'proposals', ProposalRequestViewSet, basename='proposalrequest')

urlpatterns = router.urls
