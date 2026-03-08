from pathlib import Path


def test_django_project_scaffold_exists() -> None:
    base = Path("gexable_esg/apps/django_project")
    assert (base / "manage.py").exists()
    assert (base / "config/settings/base.py").exists()
    assert (base / "config/settings/dev.py").exists()
    assert (base / "config/settings/prod.py").exists()
    assert (base / "core_api/views.py").exists()
    assert (base / ".env.example").exists()


def test_users_initial_migration_exists() -> None:
    assert Path("gexable_esg/apps/django_project/apps/users/migrations/0001_initial.py").exists()
