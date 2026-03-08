from django.urls import path

from .views import (
    AuditActionsView,
    DecarbonizationProjectsView,
    EmissionsOverviewView,
    EnergyBySiteView,
    RenewablePerformanceView,
    ScopeTrendsView,
    SupplierBenchmarkingView,
    TariffAnalysisView,
)

urlpatterns = [
    path("emissions-overview", EmissionsOverviewView.as_view(), name="dashboard-emissions-overview"),
    path("scope-trends", ScopeTrendsView.as_view(), name="dashboard-scope-trends"),
    path("energy-by-site", EnergyBySiteView.as_view(), name="dashboard-energy-by-site"),
    path("tariff-analysis", TariffAnalysisView.as_view(), name="dashboard-tariff-analysis"),
    path("renewable-performance", RenewablePerformanceView.as_view(), name="dashboard-renewable-performance"),
    path("decarbonization-projects", DecarbonizationProjectsView.as_view(), name="dashboard-decarbonization-projects"),
    path("supplier-benchmarking", SupplierBenchmarkingView.as_view(), name="dashboard-supplier-benchmarking"),
    path("audit-actions", AuditActionsView.as_view(), name="dashboard-audit-actions"),
]
