from __future__ import annotations

from django.http import HttpRequest, HttpResponse

from .tenant import reset_current_tenant, set_current_tenant


class TenantContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        tenant_id = request.headers.get("X-Tenant-ID", "default")
        request.tenant_id = tenant_id
        token = set_current_tenant(tenant_id)
        try:
            return self.get_response(request)
        finally:
            reset_current_tenant(token)


class RoleContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.gexable_role = request.headers.get("X-User-Role", "preparer")
        return self.get_response(request)
