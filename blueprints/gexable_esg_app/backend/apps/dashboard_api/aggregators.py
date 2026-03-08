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
