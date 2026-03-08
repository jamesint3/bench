from rest_framework.response import Response
from rest_framework.views import APIView

from .aggregators import DashboardAggregator


class DashboardBaseView(APIView):
    aggregator = DashboardAggregator()

    def period(self, request) -> str:
        return request.query_params.get("period", "current")


class EmissionsOverviewView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.emissions_overview(period=self.period(request), site=request.query_params.get("site", "all")))


class ScopeTrendsView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.scope_trends(period=self.period(request), site=request.query_params.get("site", "all")))


class EnergyBySiteView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.energy_by_site(period=self.period(request)))


class TariffAnalysisView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.tariff_analysis(period=self.period(request)))


class RenewablePerformanceView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.renewable_performance(period=self.period(request)))


class DecarbonizationProjectsView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.decarbonization_projects(period=self.period(request)))


class SupplierBenchmarkingView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.supplier_benchmarking(period=self.period(request)))


class AuditActionsView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.audit_actions(period=self.period(request)))
