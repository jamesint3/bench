from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmissionFactorViewSet, EmissionRecordViewSet

router = DefaultRouter()
router.register("factors", EmissionFactorViewSet, basename="emission-factor")
router.register("records", EmissionRecordViewSet, basename="emission-record")

urlpatterns = [
    path("", include(router.urls)),
]
