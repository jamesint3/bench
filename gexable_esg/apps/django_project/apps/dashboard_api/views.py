from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.request_context import get_tenant_id

from .aggregators import DashboardAggregator


class DashboardBaseView(APIView):
    aggregator = DashboardAggregator()

    def period(self, request) -> str:
        return request.query_params.get("period", "current")

    def tenant_id(self, request):
        return get_tenant_id(request)


class EmissionsOverviewView(DashboardBaseView):
    def get(self, request):
        return Response(
            self.aggregator.emissions_overview(
                tenant_id=self.tenant_id(request),
                period=self.period(request),
                site=request.query_params.get("site", "all"),
            )
        )


class ScopeTrendsView(DashboardBaseView):
    def get(self, request):
        return Response(
            self.aggregator.scope_trends(
                tenant_id=self.tenant_id(request),
                period=self.period(request),
                site=request.query_params.get("site", "all"),
            )
        )


class EnergyBySiteView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.energy_by_site(tenant_id=self.tenant_id(request), period=self.period(request)))


class TariffAnalysisView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.tariff_analysis(tenant_id=self.tenant_id(request), period=self.period(request)))


class RenewablePerformanceView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.renewable_performance(tenant_id=self.tenant_id(request), period=self.period(request)))


class DecarbonizationProjectsView(DashboardBaseView):
    def get(self, request):
        return Response(
            self.aggregator.decarbonization_projects(tenant_id=self.tenant_id(request), period=self.period(request))
        )


class SupplierBenchmarkingView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.supplier_benchmarking(tenant_id=self.tenant_id(request), period=self.period(request)))


class AuditActionsView(DashboardBaseView):
    def get(self, request):
        return Response(self.aggregator.audit_actions(tenant_id=self.tenant_id(request), period=self.period(request)))
