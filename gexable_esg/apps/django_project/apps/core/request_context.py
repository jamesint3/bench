from __future__ import annotations

from uuid import UUID

from django.http import HttpRequest


TENANT_HEADER = "X-Tenant-ID"


def get_tenant_id(request: HttpRequest) -> UUID | None:
    raw = request.headers.get(TENANT_HEADER) or request.query_params.get("tenant_id")
    if not raw and hasattr(request, "data"):
        raw = request.data.get("tenant_id")
    if not raw:
        return None
    try:
        return UUID(str(raw))
    except (TypeError, ValueError):
        return None
