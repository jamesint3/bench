from django.urls import path

from .views import ExportJobListCreateView, ReportRunDeliveryView, ReportRunListCreateView, ReportTemplateListCreateView

urlpatterns = [
    path("templates", ReportTemplateListCreateView.as_view(), name="reporting-templates"),
    path("runs", ReportRunListCreateView.as_view(), name="reporting-runs"),
    path("runs/<int:run_id>/deliver", ReportRunDeliveryView.as_view(), name="reporting-runs-deliver"),
    path("exports", ExportJobListCreateView.as_view(), name="reporting-exports"),
]
