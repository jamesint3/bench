from rest_framework import viewsets
from rest_framework.response import Response

from apps.core.request_context import get_tenant_id

from .models import Audit


class AuditViewSet(viewsets.ViewSet):
    def list(self, request):
        tenant_id = get_tenant_id(request)
        audits = Audit.objects.filter(tenant_id=tenant_id) if tenant_id else Audit.objects.none()
        return Response(list(audits.values("id", "name", "audit_type", "audit_date", "auditor_name", "status", "site_id")))
