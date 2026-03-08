from rest_framework import viewsets
from rest_framework.response import Response

from .models import DecarbonizationProject


class ProjectViewSet(viewsets.ViewSet):
    def list(self, request):
        projects = DecarbonizationProject.objects.all().values(
            "id",
            "name",
            "category",
            "status",
            "planned_start_date",
            "planned_end_date",
            "expected_abatement_tco2e",
            "actual_abatement_tco2e",
        )
        return Response(list(projects))
