from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.request_context import get_tenant_id

from .models import MeterReading, Site


class SiteViewSet(viewsets.ViewSet):
    def list(self, request):
        tenant_id = get_tenant_id(request)
        sites = Site.objects.filter(tenant_id=tenant_id) if tenant_id else Site.objects.none()
        return Response(list(sites.values("id", "name", "code", "country", "region", "site_type", "status")))

    @action(detail=True, methods=["get"], url_path="energy")
    def energy(self, request, pk=None):
        tenant_id = get_tenant_id(request)
        readings = MeterReading.objects.none()
        if tenant_id:
            readings = MeterReading.objects.filter(tenant_id=tenant_id, meter__site_id=pk).values(
                "reading_timestamp", "value", "unit", "quality_flag"
            )[:500]
        return Response({"site_id": pk, "readings": list(readings)})
