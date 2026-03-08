from celery import shared_task

from .selectors import EmissionSelectors


@shared_task
def refresh_tenant_emission_summary(tenant_id: str) -> dict[str, float | str]:
    """Celery job to compute snapshot totals for downstream KPI tasks."""
    total = EmissionSelectors.total_emissions_for_tenant(tenant_id)
    return {"tenant_id": tenant_id, "total_emissions_tco2e": total}
