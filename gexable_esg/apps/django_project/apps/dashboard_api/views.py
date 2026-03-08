from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .aggregators import DashboardAggregator
from .serializers import EmissionsOverviewSerializer


class EmissionsOverviewViewSet(ViewSet):
    aggregator = DashboardAggregator()

    def list(self, request):
        period = request.query_params.get("period", "current")
        site = request.query_params.get("site", "all")
        payload = self.aggregator.emissions_overview(period=period, site=site)
        serializer = EmissionsOverviewSerializer(payload)
        return Response(serializer.data)
