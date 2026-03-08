from celery import shared_task


@shared_task
def calculate_scope1_emissions(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "scope": "scope_1", "status": "calculated"}


@shared_task
def calculate_scope2_emissions(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "scope": "scope_2", "status": "calculated"}


@shared_task
def calculate_scope3_emissions(tenant_id: str) -> dict[str, str]:
    return {"tenant_id": tenant_id, "scope": "scope_3", "status": "calculated"}
