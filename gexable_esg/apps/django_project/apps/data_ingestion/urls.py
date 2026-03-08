from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ImportViewSet

router = DefaultRouter()
router.register("imports/jobs", ImportViewSet, basename="imports-jobs")

urlpatterns = [
    path("", include(router.urls)),
    path("imports/upload", ImportViewSet.as_view({"post": "upload"}), name="imports-upload"),
    path("imports/validate", ImportViewSet.as_view({"post": "validate"}), name="imports-validate"),
    path("imports/process", ImportViewSet.as_view({"post": "process"}), name="imports-process"),
]
