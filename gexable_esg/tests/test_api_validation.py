import pytest

from gexable_esg.apps.django_project.core_api.validators import (
    ValidationError,
    validate_activity_payload,
    validate_calculation_payload,
    validate_disclosure_payload,
)


def test_validate_activity_payload_requires_fields() -> None:
    with pytest.raises(ValidationError):
        validate_activity_payload({})


def test_validate_activity_payload_quantity_positive() -> None:
    with pytest.raises(ValidationError):
        validate_activity_payload({"site_id": "A", "quantity": 0})


def test_validate_calculation_payload_valid() -> None:
    validate_calculation_payload({"quantity": 12.5})


def test_validate_disclosure_payload_framework_restriction() -> None:
    with pytest.raises(ValidationError):
        validate_disclosure_payload({"framework": "UNKNOWN"})
