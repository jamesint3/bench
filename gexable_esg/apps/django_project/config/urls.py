from django.urls import include, path

from core_api.views import home

urlpatterns = [
    path("", home, name="home"),
    path("api/v1/", include("core_api.urls")),
]
