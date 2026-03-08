from rest_framework import viewsets
from rest_framework.response import Response

from .models import Audit


class AuditViewSet(viewsets.ViewSet):
    def list(self, request):
        audits = Audit.objects.all().values("id", "name", "audit_type", "audit_date", "auditor_name", "status", "site_id")
        return Response(list(audits))
