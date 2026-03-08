import json

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .errors import error_response
from .services import (
    activity_records,
    audit_logs,
    bus,
    calculation,
    data_intake,
    disclosures,
    emission_results,
    idempotency_key_from_headers,
    reporting,
    tenant_id_from_headers,
)
from .validators import ValidationError, validate_activity_payload, validate_calculation_payload, validate_disclosure_payload


def _json_payload(request: HttpRequest) -> dict:
    if not request.body:
        return {}
    return json.loads(request.body.decode("utf-8"))


def health(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok", "version": "v1"})


@csrf_exempt
def ingest_activity_record(request: HttpRequest) -> JsonResponse:
    payload = _json_payload(request)
    try:
        validate_activity_payload(payload)
    except ValidationError as exc:
        return error_response("VALIDATION_ERROR", str(exc), 400, exc.details)

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
        audit_logs.log(
            tenant_id=tenant_id,
            action="activity_record.ingested",
            entity_type="ActivityRecord",
            entity_id=str(persisted.id),
            payload={"source_type": persisted.source_type},
        )

    return JsonResponse(
        {
            "record": record.model_dump(),
            "persistence": {"stored": persisted is not None, "record_id": getattr(persisted, "id", None)},
        }
    )


@csrf_exempt
def calculate_emissions(request: HttpRequest) -> JsonResponse:
    payload = _json_payload(request)
    try:
        validate_calculation_payload(payload)
    except ValidationError as exc:
        return error_response("VALIDATION_ERROR", str(exc), 400, exc.details)

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
        audit_logs.log(
            tenant_id=tenant_id,
            action="emission_result.calculated",
            entity_type="EmissionResult",
            entity_id=str(persisted.id),
            payload={"scope": persisted.scope},
        )

    return JsonResponse(
        {
            "result": result.model_dump(),
            "persistence": {"stored": persisted is not None, "result_id": getattr(persisted, "id", None)},
        }
    )


@csrf_exempt
def publish_disclosure(request: HttpRequest) -> JsonResponse:
    payload = _json_payload(request)
    try:
        validate_disclosure_payload(payload)
    except ValidationError as exc:
        return error_response("VALIDATION_ERROR", str(exc), 400, exc.details)

    tenant_id = tenant_id_from_headers(request)
    report = reporting.publish(payload)
    persisted = disclosures.create(
        tenant_id=tenant_id,
        framework=report.framework,
        period=report.period,
        status=report.status,
    )
    audit_logs.log(
        tenant_id=tenant_id,
        action="disclosure.report_published",
        entity_type="DisclosureReport",
        entity_id=str(persisted.id),
        payload={"framework": persisted.framework, "period": persisted.period},
    )
    return JsonResponse({"report": report.model_dump(), "persistence": {"stored": True, "report_id": persisted.id}})


def list_events(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"events": [e.model_dump() for e in bus.events]})


def home(request: HttpRequest):
    return render(request, "core_api/index.html")


def ui_data_intake(request: HttpRequest):
    return render(request, "core_api/data_intake.html")


def ui_emissions(request: HttpRequest):
    return render(request, "core_api/emissions.html")


def ui_disclosures(request: HttpRequest):
    return render(request, "core_api/disclosures.html")


def ui_events(request: HttpRequest):
    return render(request, "core_api/events.html")


def ui_health(request: HttpRequest):
    return render(request, "core_api/health.html")


def ui_admin_portal(request: HttpRequest):
    return render(request, "core_api/admin_portal.html")
