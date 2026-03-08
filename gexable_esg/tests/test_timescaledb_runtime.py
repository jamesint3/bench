from pathlib import Path


COMPOSE_FILE = Path("docker-compose.yml")
SETTINGS_FILE = Path("gexable_esg/apps/django_project/config/settings/base.py")
DOCKERFILE = Path("Dockerfile")
BOOTSTRAP_SCRIPT = Path("gexable_esg/apps/django_project/scripts/bootstrap_runtime.sh")
APPLY_SQL_ARTIFACTS_COMMAND = Path(
    "gexable_esg/apps/django_project/core_api/management/commands/apply_sql_artifacts.py"
)
MAIN_SQL_ROOT = Path("gexable_esg/apps/django_project/db/sql")
BLUEPRINT_SQL_ROOT = Path("blueprints/gexable_esg_app/backend/db/sql")


def test_compose_includes_timescaledb_service() -> None:
    source = COMPOSE_FILE.read_text()
    assert "timescaledb:" in source
    assert "timescale/timescaledb" in source
    assert "gexable-esg-app:" in source
    assert "container_name: gexable-esg-app" in source
    assert "GEXABLE_DB_ENGINE: \"postgresql\"" in source


def test_runtime_bootstrap_runs_migrate_and_sql_artifacts() -> None:
    script = BOOTSTRAP_SCRIPT.read_text()
    assert "manage.py migrate users" in script
    assert "manage.py migrate --run-syncdb" in script
    assert "manage.py apply_sql_artifacts" in script
    assert "wait_for_db.py" in script

    assert script.index("manage.py migrate users") < script.index("manage.py migrate --run-syncdb")


def test_apply_sql_artifacts_skips_timescaledb_when_unavailable() -> None:
    source = APPLY_SQL_ARTIFACTS_COMMAND.read_text()
    assert "timescaledb.control" in source
    assert "Skipping SQL artifact because TimescaleDB is unavailable" in source


def test_apply_sql_artifacts_skips_missing_relation_dependencies() -> None:
    source = APPLY_SQL_ARTIFACTS_COMMAND.read_text()
    assert '"does not exist" in message and "relation" in message' in source
    assert "Skipping SQL artifact because dependent tables are unavailable" in source


def test_settings_support_postgresql_engine_switch() -> None:
    source = SETTINGS_FILE.read_text()
    assert 'DB_ENGINE = _env("GEXABLE_DB_ENGINE", "sqlite3").lower()' in source
    assert '"ENGINE": "django.db.backends.postgresql"' in source


def test_settings_mark_unmigrated_local_apps_for_syncdb() -> None:
    source = SETTINGS_FILE.read_text()
    assert "UNMIGRATED_LOCAL_APPS" in source
    assert '"analytics"' in source
    assert '"audits_actions"' in source
    assert "MIGRATION_MODULES = {app_label: None for app_label in UNMIGRATED_LOCAL_APPS}" in source


def test_dockerfile_uses_runtime_bootstrap_script() -> None:
    source = DOCKERFILE.read_text()
    assert "psycopg2-binary" in source
    assert "bootstrap_runtime.sh" in source


def test_main_sql_artifacts_match_blueprint_sql_artifacts() -> None:
    main_files = {p.relative_to(MAIN_SQL_ROOT).as_posix() for p in MAIN_SQL_ROOT.rglob("*.sql")}
    blueprint_files = {p.relative_to(BLUEPRINT_SQL_ROOT).as_posix() for p in BLUEPRINT_SQL_ROOT.rglob("*.sql")}

    assert main_files == blueprint_files

    for relative in sorted(main_files):
        assert (MAIN_SQL_ROOT / relative).read_text() == (BLUEPRINT_SQL_ROOT / relative).read_text()
