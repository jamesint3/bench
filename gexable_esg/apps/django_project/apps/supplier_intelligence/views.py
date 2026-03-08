from rest_framework import viewsets
from rest_framework.response import Response

from .models import Supplier


class SupplierViewSet(viewsets.ViewSet):
    def list(self, request):
        suppliers = Supplier.objects.all().values("id", "name", "country", "industry", "active_flag")
        return Response(list(suppliers))
