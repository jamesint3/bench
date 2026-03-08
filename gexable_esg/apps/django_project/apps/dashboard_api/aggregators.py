from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db.models import Avg, Count, Sum

from apps.analytics.models import (
    FactEmissionsMonthly,
    FactTariffCosts,
    KPIEmissionsOverview,
    KPIEnergySiteMonthly,
    KPIRenewablePerformance,
    KPISupplierBenchmark,
)
from apps.audits_actions.models import CorrectiveAction
from apps.decarbonization.models import DecarbonizationProject


class DashboardAggregator:
    """Endpoint-specific aggregation layer for prepared KPI/fact payloads."""

    def emissions_overview(self, *, tenant_id: UUID | None, period: str, site: str = "all") -> dict[str, Any]:
        filters: dict[str, Any] = {"tenant_id": tenant_id}
        if site != "all":
            filters["site_id"] = site
        emission_qs = FactEmissionsMonthly.objects.filter(**filters) if tenant_id else FactEmissionsMonthly.objects.none()

        by_scope = {
            row["scope"]: row["total"]
            for row in emission_qs.values("scope").annotate(total=Sum("emissions_tco2e"))
        }
        latest_kpi = (
            KPIEmissionsOverview.objects.filter(tenant_id=tenant_id).order_by("-last_refreshed_at").first()
            if tenant_id
            else None
        )

        return {
            "filters": {"period": period, "site": site},
            "summary": {
                "total_emissions_tco2e": latest_kpi.total_emissions_tco2e if latest_kpi else sum(by_scope.values(), Decimal("0")),
                "scope1_tco2e": by_scope.get("scope1", Decimal("0")),
                "scope2_tco2e": by_scope.get("scope2", Decimal("0")),
                "scope3_tco2e": by_scope.get("scope3", Decimal("0")),
            },
            "trend": list(
                emission_qs.values("year", "month").annotate(total=Sum("emissions_tco2e")).order_by("year", "month")
            ),
            "breakdown": list(emission_qs.values("category").annotate(total=Sum("emissions_tco2e")).order_by("-total")),
        }

    def scope_trends(self, *, tenant_id: UUID | None, period: str, site: str = "all") -> dict[str, Any]:
        filters: dict[str, Any] = {"tenant_id": tenant_id}
        if site != "all":
            filters["site_id"] = site
        emission_qs = FactEmissionsMonthly.objects.filter(**filters) if tenant_id else FactEmissionsMonthly.objects.none()
        trend = (
            emission_qs.values("year", "month", "scope").annotate(total=Sum("emissions_tco2e")).order_by("year", "month", "scope")
        )
        return {"filters": {"period": period, "site": site}, "trend": list(trend)}

    def energy_by_site(self, *, tenant_id: UUID | None, period: str) -> dict[str, Any]:
        qs = KPIEnergySiteMonthly.objects.filter(tenant_id=tenant_id) if tenant_id else KPIEnergySiteMonthly.objects.none()
        return {
            "filters": {"period": period},
            "sites": list(
                qs.values("site_id", "site__name")
                .annotate(energy_kwh=Sum("energy_kwh"), cost_amount=Sum("cost_amount"), renewable_share_pct=Avg("renewable_share_pct"))
                .order_by("site__name")
            ),
        }

    def tariff_analysis(self, *, tenant_id: UUID | None, period: str) -> dict[str, Any]:
        qs = FactTariffCosts.objects.filter(tenant_id=tenant_id) if tenant_id else FactTariffCosts.objects.none()
        cost_breakdown = qs.aggregate(
            energy_charge=Sum("energy_charge"),
            demand_charge=Sum("demand_charge"),
            fixed_charge=Sum("fixed_charge"),
            other_charge=Sum("other_charge"),
            total_cost=Sum("total_cost"),
        )
        return {"filters": {"period": period}, "cost_breakdown": cost_breakdown}

    def renewable_performance(self, *, tenant_id: UUID | None, period: str) -> dict[str, Any]:
        qs = KPIRenewablePerformance.objects.filter(tenant_id=tenant_id) if tenant_id else KPIRenewablePerformance.objects.none()
        return {
            "filters": {"period": period},
            "assets": list(
                qs.values("asset_id", "asset__name", "site__name")
                .annotate(generation_kwh=Sum("generation_kwh"), availability_pct=Avg("availability_pct"))
                .order_by("asset__name")
            ),
        }

    def decarbonization_projects(self, *, tenant_id: UUID | None, period: str) -> dict[str, Any]:
        qs = DecarbonizationProject.objects.filter(tenant_id=tenant_id) if tenant_id else DecarbonizationProject.objects.none()
        return {
            "filters": {"period": period},
            "projects": list(
                qs.values("id", "name", "status", "category")
                .annotate(
                    expected_abatement_tco2e=Sum("expected_abatement_tco2e"),
                    actual_abatement_tco2e=Sum("actual_abatement_tco2e"),
                )
                .order_by("name")
            ),
        }

    def supplier_benchmarking(self, *, tenant_id: UUID | None, period: str) -> dict[str, Any]:
        qs = KPISupplierBenchmark.objects.filter(tenant_id=tenant_id) if tenant_id else KPISupplierBenchmark.objects.none()
        return {
            "filters": {"period": period},
            "suppliers": list(
                qs.values("supplier_id", "supplier__name")
                .annotate(
                    emissions_tco2e=Sum("emissions_tco2e"),
                    emissions_intensity=Avg("emissions_intensity"),
                    data_quality_score=Avg("data_quality_score"),
                    peer_percentile=Avg("peer_percentile"),
                )
                .order_by("supplier__name")
            ),
        }

    def audit_actions(self, *, tenant_id: UUID | None, period: str) -> dict[str, Any]:
        qs = CorrectiveAction.objects.filter(tenant_id=tenant_id) if tenant_id else CorrectiveAction.objects.none()
        return {
            "filters": {"period": period},
            "actions": list(qs.values("status").annotate(total=Count("id")).order_by("status")),
        }
