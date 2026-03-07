from pathlib import Path


def test_django_project_scaffold_exists() -> None:
    base = Path("gexable_esg/apps/django_project")
    assert (base / "manage.py").exists()
    assert (base / "config/settings.py").exists()
    assert (base / "core_api/views.py").exists()
