from __future__ import annotations

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import EmissionFactor, EmissionRecord, EmissionSource
from .permissions import CanManageEmissions
from .serializers import (
    EmissionCalculationSerializer,
    EmissionFactorSerializer,
    EmissionRecordSerializer,
)
from .services import EmissionCalculationInput, EmissionCalculationService


class EmissionFactorViewSet(viewsets.ModelViewSet):
    queryset = EmissionFactor.objects.all()
    serializer_class = EmissionFactorSerializer
    permission_classes = [CanManageEmissions]


class EmissionRecordViewSet(viewsets.ModelViewSet):
    queryset = EmissionRecord.objects.select_related("source", "factor")
    serializer_class = EmissionRecordSerializer
    permission_classes = [CanManageEmissions]

    @action(detail=False, methods=["post"], url_path="calculate")
    def calculate(self, request):
        serializer = EmissionCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        source = EmissionSource.objects.get(pk=data["source_id"])
        factor = EmissionFactor.objects.get(pk=data["factor_id"])
        record = EmissionCalculationService.calculate_and_store(
            EmissionCalculationInput(
                tenant_id=str(data["tenant_id"]),
                source=source,
                factor=factor,
                activity_date=data["activity_date"],
                activity_amount=data["activity_amount"],
                activity_unit=data["activity_unit"],
            )
        )
        return Response(EmissionRecordSerializer(record).data, status=status.HTTP_201_CREATED)
