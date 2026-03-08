from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MeterReading, Site


class SiteViewSet(viewsets.ViewSet):
    def list(self, request):
        sites = Site.objects.all().values("id", "name", "code", "country", "region", "site_type", "status")
        return Response(list(sites))

    @action(detail=True, methods=["get"], url_path="energy")
    def energy(self, request, pk=None):
        readings = MeterReading.objects.filter(meter__site_id=pk).values("reading_timestamp", "value", "unit", "quality_flag")[:500]
        return Response({"site_id": pk, "readings": list(readings)})
