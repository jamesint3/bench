from pathlib import Path


DJANGO_APPS = Path("gexable_esg/apps/django_project/apps")
DJANGO_SQL = Path("gexable_esg/apps/django_project/db/sql")


def test_blueprint_apps_copied_into_main_django_project() -> None:
    expected_apps = {
        "core",
        "tenants",
        "users",
        "permissions",
        "data_ingestion",
        "emissions_management",
        "energy_management",
        "decarbonization",
        "supplier_intelligence",
        "audits_actions",
        "analytics",
        "reporting",
        "dashboard_api",
    }
    existing = {p.name for p in DJANGO_APPS.iterdir() if p.is_dir()}
    assert expected_apps.issubset(existing)


def test_main_django_project_contains_materialized_view_sql() -> None:
    mv_dir = DJANGO_SQL / "materialized_views"
    expected = {
        "mv_scope_trends_12m.sql",
        "mv_energy_site_comparison.sql",
        "mv_tariff_cost_monthly.sql",
        "mv_supplier_rankings.sql",
        "mv_project_progress.sql",
        "mv_audit_closure_trend.sql",
    }
    existing = {p.name for p in mv_dir.glob("*.sql")}
    assert expected.issubset(existing)


def test_main_django_project_timescaledb_script_present() -> None:
    script = DJANGO_SQL / "functions" / "timescaledb_hypertables.sql"
    text = script.read_text()
    assert "create_hypertable('meter_readings_raw'" in text
    assert "create_hypertable('renewable_generation_raw'" in text
    assert "create_hypertable('battery_dispatch_raw'" in text
