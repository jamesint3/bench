from pathlib import Path


def test_demo_ui_template_exists() -> None:
    template = Path("gexable_esg/apps/django_project/core_api/templates/core_api/index.html")
    assert template.exists()
    html = template.read_text()
    assert "Gexable ESG — Demo UI" in html
    assert "Run demo sequence" in html
