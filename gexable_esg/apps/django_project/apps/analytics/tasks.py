from celery import shared_task


@shared_task
def refresh_kpi_emissions_overview(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "kpi": "emissions_overview", "status": "refreshed"}


@shared_task
def refresh_kpi_energy_site_monthly(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "kpi": "energy_site_monthly", "status": "refreshed"}


@shared_task
def refresh_materialized_views(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "task": "materialized_views", "status": "refreshed"}


@shared_task
def run_monthly_forecast(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "task": "monthly_forecast", "status": "completed"}


@shared_task
def detect_energy_anomalies(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "task": "energy_anomalies", "status": "completed"}
