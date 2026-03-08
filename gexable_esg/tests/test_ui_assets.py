from pathlib import Path


def _assert_template_contains(path: str, snippets: list[str]) -> None:
    template = Path(path)
    assert template.exists()
    html = template.read_text()
    for snippet in snippets:
        assert snippet in html


def test_demo_ui_templates_exist() -> None:
    _assert_template_contains(
        "gexable_esg/apps/django_project/core_api/templates/core_api/index.html",
        ["Gexable ESG — Demo UI", "Admin Portal"],
    )
    _assert_template_contains(
        "gexable_esg/apps/django_project/core_api/templates/core_api/data_intake.html",
        ["Data Intake", "Submit Activity Record"],
    )
    _assert_template_contains(
        "gexable_esg/apps/django_project/core_api/templates/core_api/emissions.html",
        ["Emissions Calculation", "Calculate"],
    )
    _assert_template_contains(
        "gexable_esg/apps/django_project/core_api/templates/core_api/disclosures.html",
        ["Disclosures", "Publish Disclosure"],
    )
    _assert_template_contains(
        "gexable_esg/apps/django_project/core_api/templates/core_api/events.html",
        ["Event Stream", "Refresh Events"],
    )
    _assert_template_contains(
        "gexable_esg/apps/django_project/core_api/templates/core_api/health.html",
        ["Health", "Loading..."],
    )
    _assert_template_contains(
        "gexable_esg/apps/django_project/core_api/templates/core_api/admin_portal.html",
        ["Admin Portal", "Open Django Admin"],
    )


def test_admin_registration_file_exists() -> None:
    admin_py = Path("gexable_esg/apps/django_project/core_api/admin.py")
    assert admin_py.exists()
    content = admin_py.read_text()
    assert "admin.site.register(Organization)" in content
