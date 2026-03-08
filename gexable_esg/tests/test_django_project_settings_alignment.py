from pathlib import Path


SETTINGS_FILE = Path("gexable_esg/apps/django_project/config/settings/base.py")
URLS_FILE = Path("gexable_esg/apps/django_project/config/urls.py")


def test_settings_include_blueprint_apps_and_custom_user_model() -> None:
    source = SETTINGS_FILE.read_text()
    for app in (
        '"apps.core"',
        '"apps.tenants"',
        '"apps.users"',
        '"apps.permissions"',
        '"apps.data_ingestion"',
        '"apps.emissions_management"',
        '"apps.energy_management"',
        '"apps.decarbonization"',
        '"apps.supplier_intelligence"',
        '"apps.audits_actions"',
        '"apps.analytics"',
        '"apps.reporting"',
        '"apps.dashboard_api"',
    ):
        assert app in source
    assert 'AUTH_USER_MODEL = "users.User"' in source


def test_urls_include_dashboard_and_emissions_routes() -> None:
    source = URLS_FILE.read_text()
    assert 'path("api/dashboard/", include("apps.dashboard_api.urls"))' in source
    assert 'path("api/emissions/", include("apps.emissions_management.urls"))' in source
