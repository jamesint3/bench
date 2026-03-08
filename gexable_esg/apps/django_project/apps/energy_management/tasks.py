from celery import shared_task


@shared_task
def aggregate_daily_energy(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "aggregation": "daily", "status": "completed"}


@shared_task
def aggregate_monthly_energy(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "aggregation": "monthly", "status": "completed"}


@shared_task
def calculate_tariff_costs(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "task": "tariff_costs", "status": "completed"}
