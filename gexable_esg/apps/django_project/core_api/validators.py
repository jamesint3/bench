
class ValidationError(Exception):
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


def validate_activity_payload(payload: dict) -> None:
    required = ["site_id", "quantity"]
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValidationError("Missing required fields", {"missing": missing})

    quantity = float(payload["quantity"])
    if quantity <= 0:
        raise ValidationError("quantity must be greater than zero", {"field": "quantity"})


def validate_calculation_payload(payload: dict) -> None:
    if "quantity" not in payload:
        raise ValidationError("Missing required fields", {"missing": ["quantity"]})

    quantity = float(payload["quantity"])
    if quantity <= 0:
        raise ValidationError("quantity must be greater than zero", {"field": "quantity"})


def validate_disclosure_payload(payload: dict) -> None:
    framework = payload.get("framework", "")
    if framework and framework not in {"CSRD", "ISSB", "GRI", "CDP", "SEC"}:
        raise ValidationError(
            "Unsupported disclosure framework",
            {"framework": framework, "allowed": ["CSRD", "ISSB", "GRI", "CDP", "SEC"]},
        )
