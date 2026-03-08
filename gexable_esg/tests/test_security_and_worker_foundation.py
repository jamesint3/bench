from pathlib import Path


def test_tenant_and_role_middleware_configured() -> None:
    settings_text = Path("gexable_esg/apps/django_project/config/settings/base.py").read_text()
    assert "core_api.middleware.TenantContextMiddleware" in settings_text
    assert "core_api.middleware.RoleContextMiddleware" in settings_text


def test_role_permission_and_user_roles_exist() -> None:
    permissions = Path("gexable_esg/apps/django_project/core_api/permissions.py").read_text()
    models = Path("gexable_esg/apps/django_project/core_api/models.py").read_text()
    api_views = Path("gexable_esg/apps/django_project/core_api/api_views.py").read_text()

    assert "class RolePermission" in permissions
    assert "class UserRole" in models
    assert "required_roles" in api_views


def test_outbox_worker_command_exists() -> None:
    cmd = Path("gexable_esg/apps/django_project/core_api/management/commands/publish_outbox.py").read_text()
    repos = Path("gexable_esg/apps/django_project/core_api/repositories.py").read_text()
    migration = Path("gexable_esg/apps/django_project/core_api/migrations/0003_roles_outbox_error.py").read_text()

    assert "class Command(BaseCommand)" in cmd
    assert "def mark_error" in repos
    assert "error_message" in migration
