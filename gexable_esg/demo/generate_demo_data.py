from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

TENANT_ID = "11111111-1111-1111-1111-111111111111"


def _record(model: str, pk: int, **fields: Any) -> dict[str, Any]:
    payload = {"model": model, "pk": pk, "fields": {"tenant_id": TENANT_ID, **fields}}
    return payload


def build_demo_fixture() -> list[dict[str, Any]]:
    fixture: list[dict[str, Any]] = []

    # tenants/users/permissions
    fixture.append(
        {"model": "tenants.tenant", "pk": 1, "fields": {"name": "Acme ESG", "slug": "acme-esg", "industry": "manufacturing", "country": "DE", "timezone": "UTC", "status": "active"}}
    )
    fixture.append(
        {"model": "users.user", "pk": 1, "fields": {"email": "admin@acme-esg.demo", "password_hash": "demo-not-for-prod", "first_name": "Admin", "last_name": "User", "is_active": True, "is_superuser": True}}
    )
    fixture.append(_record("permissions.permission", 1, key="dashboard.view", module="dashboard", action="view", scope="tenant"))
    fixture.append(_record("permissions.role", 1, tenant=1, name="esg_manager", description="Demo ESG manager role"))
    fixture.append(_record("permissions.rolepermission", 1, role=1, permission=1))
    fixture.append(_record("permissions.userroleassignment", 1, user=1, tenant=1, role=1, site=None))

    # energy_management
    fixture.append(_record("energy_management.site", 1, name="Berlin Plant", code="BER-01", country="DE", region="Berlin", site_type="manufacturing", floor_area_m2="12000.00", production_unit="widget", status="active"))
    fixture.append(_record("energy_management.meter", 1, site=1, meter_name="Main Grid Meter", meter_type="electricity", unit="kWh", interval_minutes=60, source_system="utility_api", status="active"))
    fixture.append(_record("energy_management.meterreading", 1, meter=1, reading_timestamp="2026-01-01T00:00:00Z", value="325.500000", unit="kWh", quality_flag="validated", source_file_id=1))
    fixture.append(_record("energy_management.tariffplan", 1, site=1, name="Industrial TOU", currency="EUR", valid_from="2026-01-01", valid_to=None))
    fixture.append(_record("energy_management.utilitybill", 1, site=1, billing_period_start="2026-01-01", billing_period_end="2026-01-31", utility_type="electricity", consumption="86000.000000", consumption_unit="kWh", cost_amount="13350.00", currency="EUR", demand_charge="2000.00", source_file_id=1))
    fixture.append(_record("energy_management.renewableasset", 1, site=1, asset_type="solar_pv", name="Roof PV", capacity_kw="600.00", commission_date="2024-06-01", status="active"))
    fixture.append(_record("energy_management.batteryasset", 1, site=1, name="Battery A", power_kw="250.00", energy_kwh="500.00", round_trip_efficiency="92.00", status="active"))

    # supplier_intelligence
    fixture.append(_record("supplier_intelligence.suppliercategory", 1, name="Logistics", description="Transport partners"))
    fixture.append(_record("supplier_intelligence.supplier", 1, name="Eco Logistics GmbH", supplier_category=1, country="DE", industry="logistics", active_flag=True))
    fixture.append(_record("supplier_intelligence.supplieractivityraw", 1, supplier=1, activity_date="2026-01-10", activity_type="road_freight", quantity="14000.000000", unit="tkm", spend_amount="42000.00", currency="EUR", source_file_id=2))
    fixture.append(_record("supplier_intelligence.supplierdisclosure", 1, supplier=1, period_start="2026-01-01", period_end="2026-03-31", emissions_tco2e="75.200000", data_quality_score="88.50"))
    fixture.append(_record("supplier_intelligence.supplierscorecard", 1, supplier=1, period_start="2026-01-01", period_end="2026-03-31", score="82.30", engagement_status="active"))
    fixture.append(_record("supplier_intelligence.supplierbenchmark", 1, supplier=1, period_start="2026-01-01", period_end="2026-03-31", emissions_intensity="0.005300", peer_percentile="74.00"))

    # emissions_management
    fixture.append(_record("emissions_management.scopeclassification", 1, code="scope2", category="Purchased electricity", description="Grid electricity consumption"))
    fixture.append(_record("emissions_management.emissionsource", 1, name="Grid power purchase", source_type="electricity", scope_classification=1))
    fixture.append(_record("emissions_management.emissionfactor", 1, factor_code="IEA-DE-2026", scope="scope2", category="electricity", region="DE", unit_from="kWh", unit_to="tco2e", factor_value="0.00038000", factor_source="IEA", valid_from="2026-01-01", valid_to=None, version="v2026"))
    fixture.append(_record("emissions_management.emissionrecord", 1, source=1, factor=1, activity_date="2026-01-31", activity_amount="86000.000000", activity_unit="kWh", emissions_tco2e="32.680000"))
    fixture.append(_record("emissions_management.productfootprint", 1, product_code="WIDGET-X", product_name="Widget X", period_start="2026-01-01", period_end="2026-03-31", emissions_tco2e="120.300000", methodology="GHG Protocol"))

    # data_ingestion
    fixture.append(_record("data_ingestion.datasource", 1, name="Utility CSV Drop", source_type="csv", connection_ref="s3://demo-bucket/utility"))
    fixture.append(_record("data_ingestion.importjob", 1, source=1, status="succeeded", started_at="2026-01-02T08:00:00Z", completed_at="2026-01-02T08:05:00Z", row_count=900))
    fixture.append(_record("data_ingestion.importfile", 1, import_job=1, file_name="utility_jan.csv", file_uri="s3://demo-bucket/utility/utility_jan.csv", checksum="sha256-demo-001"))
    fixture.append(_record("data_ingestion.validationissue", 1, import_job=1, severity="warning", row_number=87, field_name="consumption", message="Interpolated missing value"))
    fixture.append(_record("data_ingestion.dataqualityscore", 1, import_job=1, completeness_score="97.00", validity_score="98.50", uniqueness_score="99.00", overall_score="98.17"))

    # decarbonization
    fixture.append(_record("decarbonization.decarbonizationproject", 1, site=1, name="Heat Pump Retrofit", category="electrification", status="in_progress", owner=1, capex_amount="450000.00", currency="EUR", planned_start_date="2026-02-01", planned_end_date="2026-11-30", expected_abatement_tco2e="180.000000", actual_abatement_tco2e="42.000000"))
    fixture.append(_record("decarbonization.projectmilestone", 1, project=1, title="Engineering design", due_date="2026-03-15", completed_at="2026-03-10T09:00:00Z"))
    fixture.append(_record("decarbonization.projectabatement", 1, project=1, period_start="2026-02-01", period_end="2026-02-28", expected_abatement_tco2e="15.000000", actual_abatement_tco2e="12.500000", cost_savings_amount="4800.00"))
    fixture.append(_record("decarbonization.emissiontarget", 1, target_name="2030 Scope 1+2", baseline_year=2024, target_year=2030, target_scope="scope1+scope2", target_reduction_pct="45.00", science_based_flag=True, status="active"))
    fixture.append(_record("decarbonization.scenariorun", 1, name="Accelerated electrification", assumptions={"carbon_price": 120, "growth_pct": 4}, result_summary={"abatement_tco2e": 920.5, "npv_eur": 2300000}))

    # audits_actions
    fixture.append(_record("audits_actions.audit", 1, site=1, name="ISO 14001 Internal Audit", audit_type="internal", audit_date="2026-02-20", auditor_name="R. Schmidt", status="open"))
    fixture.append(_record("audits_actions.auditfinding", 1, audit=1, site=1, severity="high", category="energy", title="Submeter coverage incomplete", description="Line 3 and 4 submeters not integrated.", status="open", due_date="2026-04-15", owner=1))
    fixture.append(_record("audits_actions.correctiveaction", 1, finding=1, title="Install missing submeters", description="Procure and commission submeters for lines 3/4.", status="in_progress", priority="high", owner=1, due_date="2026-04-05", completed_at=None))
    fixture.append(_record("audits_actions.actioncomment", 1, action=1, author=1, comment="Vendor selected and PO issued."))
    fixture.append(_record("audits_actions.actionevidence", 1, action=1, file_name="po-submeters.pdf", file_uri="s3://demo-bucket/evidence/po-submeters.pdf"))

    # analytics
    fixture.append(_record("analytics.factenergyconsumptiondaily", 1, site=1, date="2026-01-31", energy_kwh="86000.000000", peak_kw="510.000000", offpeak_kwh="24000.000000", renewable_kwh="16200.000000", grid_import_kwh="69800.000000", grid_export_kwh="1100.000000", cost_amount="13350.00", currency="EUR"))
    fixture.append(_record("analytics.factemissionsmonthly", 1, site=1, supplier=1, year=2026, month=1, scope="scope2", category="electricity", activity_amount="86000.000000", activity_unit="kWh", emissions_tco2e="32.680000", methodology="market_based", factor_version="v2026"))
    fixture.append(_record("analytics.factsupplieremissions", 1, supplier=1, period_start="2026-01-01", period_end="2026-03-31", scope3_category="category_4", emissions_tco2e="75.200000", data_quality_score="88.50", estimated_flag=False))
    fixture.append(_record("analytics.facttariffcosts", 1, site=1, date="2026-01-31", energy_charge="9800.00", demand_charge="2200.00", fixed_charge="900.00", other_charge="450.00", total_cost="13350.00", currency="EUR"))
    fixture.append(_record("analytics.kpiemissionsoverview", 1, period_type="month", period_value="2026-01", total_scope1_tco2e="9.100000", total_scope2_tco2e="32.680000", total_scope3_tco2e="75.200000", total_emissions_tco2e="116.980000", target_emissions_tco2e="110.000000", variance_tco2e="6.980000", last_refreshed_at="2026-02-01T00:30:00Z"))
    fixture.append(_record("analytics.kpienergysitemonthly", 1, site=1, year=2026, month=1, energy_kwh="86000.000000", cost_amount="13350.00", energy_intensity="7.166700", peak_kw="510.000000", renewable_share_pct="18.84", last_refreshed_at="2026-02-01T00:35:00Z"))
    fixture.append(_record("analytics.kpirenewableperformance", 1, site=1, asset=1, year=2026, month=1, generation_kwh="16200.000000", self_consumption_pct="92.50", export_kwh="1100.000000", curtailment_kwh="300.000000", availability_pct="98.20"))
    fixture.append(_record("analytics.kpisupplierbenchmark", 1, supplier=1, period_start="2026-01-01", period_end="2026-03-31", emissions_tco2e="75.200000", emissions_intensity="0.005300", data_quality_score="88.50", peer_percentile="74.00", engagement_status="active"))
    fixture.append(_record("analytics.kpiauditactions", 1, site=1, period_start="2026-01-01", period_end="2026-03-31", open_findings=6, closed_findings=11, overdue_actions=2, closure_rate_pct="64.71"))
    fixture.append(_record("analytics.materializedviewrefreshlog", 1, view_name="mv_scope_trends_12m", started_at="2026-02-01T00:25:00Z", completed_at="2026-02-01T00:26:00Z", status="succeeded", detail="refresh complete"))
    fixture.append(_record("analytics.forecastrun", 1, model_name="energy_baseline_v2", period_start="2026-02-01", period_end="2026-12-31", metrics={"mape": 0.08, "annual_energy_kwh": 1020000}))
    fixture.append(_record("analytics.anomalyevent", 1, source="meter_readings", severity="high", context={"meter_id": 1, "z_score": 4.3, "detected": "2026-02-03T05:00:00Z"}))

    # reporting
    fixture.append(_record("reporting.reporttemplate", 1, name="CSRD Monthly Pack", framework="CSRD", file_format="pdf", template_config={"sections": ["emissions", "energy", "assurance"]}))
    fixture.append(_record("reporting.reportrun", 1, template=1, requested_by=1, status="completed", output_uri="s3://demo-bucket/reports/csrd-2026-01.pdf", started_at="2026-02-02T09:00:00Z", completed_at="2026-02-02T09:04:00Z"))
    fixture.append(_record("reporting.reportrecipient", 1, report_run=1, email="board@acme-esg.demo", delivery_status="sent"))
    fixture.append(_record("reporting.exportjob", 1, report_run=1, export_type="csv", status="completed", artifact_uri="s3://demo-bucket/reports/csrd-2026-01.csv"))

    return fixture


def build_dashboard_payload_samples() -> dict[str, dict[str, object]]:
    return {
        "emissions-overview": {"filters": {"period": "current", "site": "all"}, "summary": {"total_emissions_tco2e": "116.980000", "scope1_tco2e": "9.100000", "scope2_tco2e": "32.680000", "scope3_tco2e": "75.200000"}},
        "scope-trends": {"filters": {"period": "12m", "site": "all"}, "trend": [{"year": 2026, "month": 1, "scope": "scope2", "total": "32.680000"}]},
        "energy-by-site": {"filters": {"period": "current"}, "sites": [{"site__name": "Berlin Plant", "energy_kwh": "86000.000000", "cost_amount": "13350.00"}]},
        "tariff-analysis": {"filters": {"period": "current"}, "cost_breakdown": {"total_cost": "13350.00"}},
        "renewable-performance": {"filters": {"period": "current"}, "assets": [{"asset__name": "Roof PV", "generation_kwh": "16200.000000"}]},
        "decarbonization-projects": {"filters": {"period": "current"}, "projects": [{"name": "Heat Pump Retrofit", "status": "in_progress"}]},
        "supplier-benchmarking": {"filters": {"period": "current"}, "suppliers": [{"supplier__name": "Eco Logistics GmbH", "peer_percentile": "74.00"}]},
        "audit-actions": {"filters": {"period": "current"}, "actions": [{"status": "in_progress", "total": 1}]},
    }


def summarize_by_module(fixture: list[dict[str, Any]]) -> dict[str, int]:
    grouped: dict[str, int] = defaultdict(int)
    for row in fixture:
        app_label = row["model"].split(".", 1)[0]
        grouped[app_label] += 1
    return dict(sorted(grouped.items()))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic demo fixture data across all modules.")
    parser.add_argument(
        "--output",
        default="gexable_esg/demo/demo_data_fixture.json",
        help="Where to write the generated JSON fixture.",
    )
    parser.add_argument(
        "--dashboard-output",
        default="gexable_esg/demo/dashboard_api_demo_payloads.json",
        help="Where to write dashboard endpoint sample payloads.",
    )
    args = parser.parse_args()

    fixture = build_demo_fixture()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(fixture, indent=2))

    dashboard_output = Path(args.dashboard_output)
    dashboard_output.parent.mkdir(parents=True, exist_ok=True)
    dashboard_output.write_text(json.dumps(build_dashboard_payload_samples(), indent=2))

    summary = summarize_by_module(fixture)
    print(json.dumps({"output": str(output), "dashboard_output": str(dashboard_output), "records": len(fixture), "modules": summary}, indent=2))


if __name__ == "__main__":
    main()
