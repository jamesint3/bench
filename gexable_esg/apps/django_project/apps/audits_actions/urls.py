from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuditViewSet

router = DefaultRouter()
router.register("audits", AuditViewSet, basename="audits")

urlpatterns = [
    path("", include(router.urls)),
]
