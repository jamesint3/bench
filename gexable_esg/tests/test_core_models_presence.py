from pathlib import Path


MODELS_FILE = Path("gexable_esg/apps/django_project/core_api/models.py")


def test_missing_core_models_are_defined() -> None:
    source = MODELS_FILE.read_text()

    for model_name in ("BusinessUnit", "Asset", "Control", "Approval", "Target"):
        assert f"class {model_name}(TenantStampedModel):" in source


def test_disclosure_support_models_are_defined() -> None:
    source = MODELS_FILE.read_text()

    assert "class DisclosureMetric(TenantStampedModel):" in source
    assert "class EvidenceFile(TenantStampedModel):" in source
