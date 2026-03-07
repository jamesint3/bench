import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services import bus, calculation, data_intake, reporting


def _json_payload(request: HttpRequest) -> dict:
    if not request.body:
        return {}
    return json.loads(request.body.decode("utf-8"))


def health(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


@csrf_exempt
def ingest_activity_record(request: HttpRequest) -> JsonResponse:
    payload = _json_payload(request)
    record = data_intake.ingest(payload)
    return JsonResponse({"record": record.model_dump()})


@csrf_exempt
def calculate_emissions(request: HttpRequest) -> JsonResponse:
    payload = _json_payload(request)
    result = calculation.calculate(payload)
    return JsonResponse({"result": result.model_dump()})


@csrf_exempt
def publish_disclosure(request: HttpRequest) -> JsonResponse:
    payload = _json_payload(request)
    report = reporting.publish(payload)
    return JsonResponse({"report": report.model_dump()})


def list_events(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"events": [e.model_dump() for e in bus.events]})
