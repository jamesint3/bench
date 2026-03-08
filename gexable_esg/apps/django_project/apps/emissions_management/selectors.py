from __future__ import annotations

from django.db.models import QuerySet, Sum

from .models import EmissionFactor, EmissionRecord


class EmissionSelectors:
    """Read/query logic for emission records and aggregates."""

    @staticmethod
    def factors_for_tenant(tenant_id: str) -> QuerySet[EmissionFactor]:
        return EmissionFactor.objects.filter(tenant_id=tenant_id)

    @staticmethod
    def records_for_tenant(tenant_id: str) -> QuerySet[EmissionRecord]:
        return EmissionRecord.objects.filter(tenant_id=tenant_id)

    @staticmethod
    def total_emissions_for_tenant(tenant_id: str) -> float:
        result = EmissionRecord.objects.filter(tenant_id=tenant_id).aggregate(total=Sum("emissions_tco2e"))
        return float(result["total"] or 0)
