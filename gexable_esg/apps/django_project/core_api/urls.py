from django.urls import path

from . import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("activity-records", views.ingest_activity_record, name="activity-records"),
    path("emissions/calculate", views.calculate_emissions, name="emissions-calculate"),
    path("disclosures/publish", views.publish_disclosure, name="disclosures-publish"),
    path("audit/events", views.list_events, name="audit-events"),
]
