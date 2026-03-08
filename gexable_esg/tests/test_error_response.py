import pytest


django = pytest.importorskip("django")

from gexable_esg.apps.django_project.core_api.errors import error_response


def test_error_response_payload_shape() -> None:
    response = error_response("VALIDATION_ERROR", "Invalid payload", 400, {"field": "quantity"})
    assert response.status_code == 400
    assert b'"code": "VALIDATION_ERROR"' in response.content
