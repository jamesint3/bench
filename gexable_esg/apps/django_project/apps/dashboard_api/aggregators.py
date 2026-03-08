from typing import Any


class DashboardAggregator:
    """Endpoint-specific aggregation layer for prepared KPI payloads."""

    def emissions_overview(self, *, period: str, site: str = "all") -> dict[str, Any]:
        return {
            "filters": {"period": period, "site": site},
            "summary": {
                "total_emissions_tco2e": 0,
                "scope1_tco2e": 0,
                "scope2_tco2e": 0,
                "scope3_tco2e": 0,
            },
            "trend": [],
            "breakdown": [],
        }

    def scope_trends(self, *, period: str, site: str = "all") -> dict[str, Any]:
        return {"filters": {"period": period, "site": site}, "trend": []}

    def energy_by_site(self, *, period: str) -> dict[str, Any]:
        return {"filters": {"period": period}, "sites": []}

    def tariff_analysis(self, *, period: str) -> dict[str, Any]:
        return {"filters": {"period": period}, "cost_breakdown": []}

    def renewable_performance(self, *, period: str) -> dict[str, Any]:
        return {"filters": {"period": period}, "assets": []}

    def decarbonization_projects(self, *, period: str) -> dict[str, Any]:
        return {"filters": {"period": period}, "projects": []}

    def supplier_benchmarking(self, *, period: str) -> dict[str, Any]:
        return {"filters": {"period": period}, "suppliers": []}

    def audit_actions(self, *, period: str) -> dict[str, Any]:
        return {"filters": {"period": period}, "actions": []}
