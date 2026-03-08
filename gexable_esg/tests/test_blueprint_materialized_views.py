from pathlib import Path


MV_DIR = Path("blueprints/gexable_esg_app/backend/db/sql/materialized_views")
FUNCTIONS_DIR = Path("blueprints/gexable_esg_app/backend/db/sql/functions")


def test_required_materialized_view_sql_files_exist() -> None:
    expected = {
        "mv_scope_trends_12m.sql",
        "mv_energy_site_comparison.sql",
        "mv_tariff_cost_monthly.sql",
        "mv_supplier_rankings.sql",
        "mv_project_progress.sql",
        "mv_audit_closure_trend.sql",
    }
    existing = {p.name for p in MV_DIR.glob("*.sql")}
    assert expected.issubset(existing)


def test_timescaledb_hypertable_script_mentions_required_raw_tables() -> None:
    text = (FUNCTIONS_DIR / "timescaledb_hypertables.sql").read_text()
    assert "create_hypertable('meter_readings_raw'" in text
    assert "create_hypertable('renewable_generation_raw'" in text
    assert "create_hypertable('battery_dispatch_raw'" in text
