from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmissionsOverviewViewSet

router = DefaultRouter()
router.register("emissions-overview", EmissionsOverviewViewSet, basename="emissions-overview")

urlpatterns = [
    path("", include(router.urls)),
]
