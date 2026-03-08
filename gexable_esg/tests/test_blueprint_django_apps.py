from pathlib import Path


BLUEPRINT_APPS = Path("blueprints/gexable_esg_app/backend/apps")


def test_blueprint_apps_exist_with_core_files() -> None:
    app_names = [
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
    ]
    for app in app_names:
        app_dir = BLUEPRINT_APPS / app
        assert app_dir.exists()
        for file_name in (
            "models.py",
            "services.py",
            "selectors.py",
            "tasks.py",
            "serializers.py",
            "views.py",
            "urls.py",
            "filters.py",
            "permissions.py",
            "admin.py",
            "apps.py",
        ):
            assert (app_dir / file_name).exists()
        assert (app_dir / "tests").exists()
        assert (app_dir / "migrations").exists()


def test_blueprint_model_class_presence() -> None:
    expected = {
        "tenants/models.py": ["Tenant", "TenantSettings", "TenantFeatureFlag"],
        "users/models.py": ["User", "UserProfile", "UserTenantMembership"],
        "permissions/models.py": ["Role", "Permission", "RolePermission", "UserRoleAssignment"],
        "data_ingestion/models.py": ["ImportJob", "ImportFile", "DataSource", "ValidationIssue", "DataQualityScore"],
        "emissions_management/models.py": ["EmissionSource", "EmissionFactor", "EmissionRecord", "ScopeClassification", "ProductFootprint"],
        "energy_management/models.py": ["Site", "Meter", "MeterReading", "TariffPlan", "UtilityBill", "RenewableAsset", "BatteryAsset"],
        "decarbonization/models.py": ["DecarbonizationProject", "ProjectMilestone", "ProjectAbatement", "EmissionTarget", "ScenarioRun"],
        "supplier_intelligence/models.py": ["Supplier", "SupplierActivityRaw", "SupplierDisclosure", "SupplierScorecard", "SupplierCategory", "SupplierBenchmark"],
        "audits_actions/models.py": ["Audit", "AuditFinding", "CorrectiveAction", "ActionComment", "ActionEvidence"],
        "analytics/models.py": [
            "FactEnergyConsumptionDaily",
            "FactEmissionsMonthly",
            "FactSupplierEmissions",
            "FactTariffCosts",
            "KPIEmissionsOverview",
            "KPIEnergySiteMonthly",
            "KPIRenewablePerformance",
            "KPISupplierBenchmark",
            "KPIAuditActions",
            "MaterializedViewRefreshLog",
            "ForecastRun",
            "AnomalyEvent",
        ],
        "reporting/models.py": ["ReportTemplate", "ReportRun", "ReportRecipient", "ExportJob"],
    }

    for rel_path, names in expected.items():
        source = (BLUEPRINT_APPS / rel_path).read_text()
        for name in names:
            assert f"class {name}(" in source


def test_emissions_management_contains_layer_implementations() -> None:
    base = BLUEPRINT_APPS / "emissions_management"
    assert "class EmissionCalculationService:" in (base / "services.py").read_text()
    assert "class EmissionSelectors:" in (base / "selectors.py").read_text()
    assert "def refresh_tenant_emission_summary" in (base / "tasks.py").read_text()
    assert "class EmissionRecordSerializer" in (base / "serializers.py").read_text()
    assert "class EmissionRecordViewSet" in (base / "views.py").read_text()


def test_schema_alignment_table_names_present() -> None:
    checks = {
        "tenants/models.py": ["db_table = \"tenants\""],
        "users/models.py": ["db_table = \"users\"", "db_table = \"user_tenant_memberships\""],
        "permissions/models.py": ["db_table = \"roles\""],
        "energy_management/models.py": [
            "db_table = \"sites\"",
            "db_table = \"meters\"",
            "db_table = \"meter_readings_raw\"",
            "db_table = \"utility_bills_raw\"",
            "db_table = \"renewable_assets\"",
            "db_table = \"battery_assets\"",
        ],
        "supplier_intelligence/models.py": ["db_table = \"suppliers\"", "db_table = \"supplier_activity_raw\""],
        "emissions_management/models.py": ["db_table = \"emission_factor_library\""],
        "analytics/models.py": [
            "db_table = \"fact_energy_consumption_daily\"",
            "db_table = \"fact_emissions_monthly\"",
            "db_table = \"fact_supplier_emissions\"",
            "db_table = \"fact_tariff_costs\"",
            "db_table = \"kpi_emissions_overview\"",
            "db_table = \"kpi_energy_site_monthly\"",
            "db_table = \"kpi_renewable_performance\"",
            "db_table = \"kpi_supplier_benchmark\"",
            "db_table = \"kpi_audit_actions\"",
        ],
        "decarbonization/models.py": ["db_table = \"decarbonization_projects\"", "db_table = \"emission_targets\""],
        "audits_actions/models.py": [
            "db_table = \"audits\"",
            "db_table = \"audit_findings\"",
            "db_table = \"corrective_actions\"",
        ],
    }
    for rel_path, patterns in checks.items():
        text = (BLUEPRINT_APPS / rel_path).read_text()
        for pattern in patterns:
            assert pattern in text
