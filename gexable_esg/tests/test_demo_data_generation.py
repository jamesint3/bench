import json
import subprocess
import sys
from pathlib import Path

from gexable_esg.demo.generate_demo_data import build_demo_fixture, summarize_by_module


def test_fixture_contains_records_for_each_business_module() -> None:
    fixture = build_demo_fixture()
    modules = summarize_by_module(fixture)

    expected = {
        "tenants",
        "users",
        "permissions",
        "energy_management",
        "emissions_management",
        "data_ingestion",
        "decarbonization",
        "supplier_intelligence",
        "audits_actions",
        "analytics",
        "reporting",
    }
    assert expected.issubset(modules.keys())
    assert all(modules[module] > 0 for module in expected)


def test_generator_writes_fixture_and_dashboard_payload_files(tmp_path: Path) -> None:
    fixture_path = tmp_path / "demo_fixture.json"
    dashboard_path = tmp_path / "dashboard_payloads.json"

    subprocess.run(
        [
            sys.executable,
            "gexable_esg/demo/generate_demo_data.py",
            "--output",
            str(fixture_path),
            "--dashboard-output",
            str(dashboard_path),
        ],
        check=True,
    )

    fixture = json.loads(fixture_path.read_text())
    dashboard = json.loads(dashboard_path.read_text())

    assert len(fixture) >= 50
    assert "emissions-overview" in dashboard
    assert "audit-actions" in dashboard
