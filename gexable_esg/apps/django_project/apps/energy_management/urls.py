from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SiteViewSet

router = DefaultRouter()
router.register("sites", SiteViewSet, basename="sites")

urlpatterns = [
    path("", include(router.urls)),
]
