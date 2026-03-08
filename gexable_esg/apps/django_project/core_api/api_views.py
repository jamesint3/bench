from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import RolePermission
from .repositories import AuditLogRepository, DomainEventOutboxRepository
from .serializers import ActivityRecordInSerializer, DisclosurePublishInSerializer, EmissionsCalculateInSerializer
from .services import (
    activity_records,
    bus,
    calculation,
    data_intake,
    disclosures,
    emission_results,
    idempotency_key_from_headers,
    reporting,
    tenant_id_from_headers,
)


def _validation_error(errors: dict) -> Response:
    return Response(
        {"error": {"code": "VALIDATION_ERROR", "message": "Invalid request payload", "details": errors}},
        status=status.HTTP_400_BAD_REQUEST,
    )


class HealthAPIView(APIView):
    permission_classes = [RolePermission]
    required_roles = ["preparer", "reviewer", "approver", "admin"]

    def get(self, _request):
        return Response({"status": "ok", "version": "v1"})


class ActivityRecordsAPIView(APIView):
    permission_classes = [RolePermission]
    required_roles = ["preparer", "reviewer", "approver", "admin"]

    def post(self, request):
        serializer = ActivityRecordInSerializer(data=request.data)
        if not serializer.is_valid():
            return _validation_error(serializer.errors)

        payload = serializer.validated_data
        tenant_id = tenant_id_from_headers(request)
        record = data_intake.ingest(payload)

        persisted = None
        site_id = payload.get("site_id")
        if isinstance(site_id, int):
            persisted = activity_records.create(
                tenant_id=tenant_id,
                site_id=site_id,
                quantity=float(payload["quantity"]),
                unit=payload.get("unit", "kWh"),
                source_type=payload.get("source_type", "manual_upload"),
                idempotency_key=idempotency_key_from_headers(request),
            )
            AuditLogRepository().log(
                tenant_id=tenant_id,
                action="activity_record.ingested",
                entity_type="ActivityRecord",
                entity_id=str(persisted.id),
                payload={"source_type": persisted.source_type},
            )

        DomainEventOutboxRepository().queue(
            tenant_id=tenant_id,
            topic="activity_record.ingested",
            payload=record.model_dump(),
        )
        return Response(
            {
                "record": record.model_dump(),
                "persistence": {"stored": persisted is not None, "record_id": getattr(persisted, "id", None)},
            }
        )


class EmissionsCalculateAPIView(APIView):
    permission_classes = [RolePermission]
    required_roles = ["preparer", "reviewer", "approver", "admin"]

    def post(self, request):
        serializer = EmissionsCalculateInSerializer(data=request.data)
        if not serializer.is_valid():
            return _validation_error(serializer.errors)

        payload = serializer.validated_data
        tenant_id = tenant_id_from_headers(request)
        result = calculation.calculate(payload)

        persisted = None
        activity_record_id = payload.get("activity_record_id")
        if isinstance(activity_record_id, int):
            persisted = emission_results.create(
                tenant_id=tenant_id,
                activity_record_id=activity_record_id,
                scope=payload.get("scope", "scope2"),
                co2e_kg=result.co2e_kg,
                calculation_method_version=payload.get("calculation_method_version", "v1"),
                factor_version=payload.get("factor_version", "v1"),
            )
            AuditLogRepository().log(
                tenant_id=tenant_id,
                action="emission_result.calculated",
                entity_type="EmissionResult",
                entity_id=str(persisted.id),
                payload={"scope": persisted.scope},
            )

        DomainEventOutboxRepository().queue(
            tenant_id=tenant_id,
            topic="emission_result.calculated",
            payload=result.model_dump(),
        )
        return Response(
            {
                "result": result.model_dump(),
                "persistence": {"stored": persisted is not None, "result_id": getattr(persisted, "id", None)},
            }
        )


class DisclosuresPublishAPIView(APIView):
    permission_classes = [RolePermission]
    required_roles = ["reviewer", "approver", "admin"]

    def post(self, request):
        serializer = DisclosurePublishInSerializer(data=request.data)
        if not serializer.is_valid():
            return _validation_error(serializer.errors)

        payload = serializer.validated_data
        tenant_id = tenant_id_from_headers(request)
        report = reporting.publish(payload)
        persisted = disclosures.create(
            tenant_id=tenant_id,
            framework=report.framework,
            period=report.period,
            status=report.status,
        )
        AuditLogRepository().log(
            tenant_id=tenant_id,
            action="disclosure.report_published",
            entity_type="DisclosureReport",
            entity_id=str(persisted.id),
            payload={"framework": persisted.framework, "period": persisted.period},
        )
        DomainEventOutboxRepository().queue(
            tenant_id=tenant_id,
            topic="disclosure.report_published",
            payload=report.model_dump(),
        )
        return Response({"report": report.model_dump(), "persistence": {"stored": True, "report_id": persisted.id}})


class AuditEventsAPIView(APIView):
    permission_classes = [RolePermission]
    required_roles = ["reviewer", "approver", "admin"]

    def get(self, _request):
        return Response({"events": [e.model_dump() for e in bus.events]})
