from rest_framework import viewsets
from rest_framework.response import Response

from apps.core.request_context import get_tenant_id

from .models import Supplier


class SupplierViewSet(viewsets.ViewSet):
    def list(self, request):
        tenant_id = get_tenant_id(request)
        suppliers = Supplier.objects.filter(tenant_id=tenant_id) if tenant_id else Supplier.objects.none()
        return Response(list(suppliers.values("id", "name", "country", "industry", "active_flag")))
