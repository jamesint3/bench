from pathlib import Path


MODULE_DIR = Path(__file__).resolve().parents[1]


def test_expected_module_files_exist() -> None:
    expected = {
        "admin.py",
        "apps.py",
        "models.py",
        "services.py",
        "selectors.py",
        "tasks.py",
        "serializers.py",
        "views.py",
        "urls.py",
        "filters.py",
        "permissions.py",
    }
    existing = {p.name for p in MODULE_DIR.iterdir() if p.is_file()}
    assert expected.issubset(existing)
