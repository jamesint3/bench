from rest_framework import viewsets
from rest_framework.response import Response

from apps.core.request_context import get_tenant_id

from .models import DecarbonizationProject


class ProjectViewSet(viewsets.ViewSet):
    def list(self, request):
        tenant_id = get_tenant_id(request)
        projects = DecarbonizationProject.objects.filter(tenant_id=tenant_id) if tenant_id else DecarbonizationProject.objects.none()
        return Response(
            list(
                projects.values(
                    "id",
                    "name",
                    "category",
                    "status",
                    "planned_start_date",
                    "planned_end_date",
                    "expected_abatement_tco2e",
                    "actual_abatement_tco2e",
                )
            )
        )
