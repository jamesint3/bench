from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .api_views import AuditEventsAPIView, DisclosuresPublishAPIView, EmissionsCalculateAPIView, HealthAPIView, ActivityRecordsAPIView

urlpatterns = [
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    path("docs", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("health", HealthAPIView.as_view(), name="health"),
    path("activity-records", ActivityRecordsAPIView.as_view(), name="activity-records"),
    path("emissions/calculate", EmissionsCalculateAPIView.as_view(), name="emissions-calculate"),
    path("disclosures/publish", DisclosuresPublishAPIView.as_view(), name="disclosures-publish"),
    path("audit/events", AuditEventsAPIView.as_view(), name="audit-events"),
]
