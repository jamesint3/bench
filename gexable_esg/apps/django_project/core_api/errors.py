from django.http import JsonResponse


def error_response(code: str, message: str, status: int = 400, details: dict | None = None) -> JsonResponse:
    payload = {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        }
    }
    return JsonResponse(payload, status=status)
