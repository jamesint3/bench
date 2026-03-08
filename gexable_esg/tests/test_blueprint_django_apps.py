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
        assert (app_dir / "models.py").exists()
        assert (app_dir / "services.py").exists()
        assert (app_dir / "selectors.py").exists()
        assert (app_dir / "tasks.py").exists()


def test_blueprint_model_class_presence() -> None:
    expected = {
        "tenants/models.py": ["Tenant", "TenantSettings", "TenantFeatureFlag"],
        "users/models.py": ["User", "UserProfile", "UserTenantMembership"],
        "permissions/models.py": ["Role", "Permission", "RolePermission", "UserRoleAssignment"],
        "data_ingestion/models.py": ["ImportJob", "ImportFile", "DataSource", "ValidationIssue", "DataQualityScore"],
        "emissions_management/models.py": ["EmissionSource", "EmissionFactor", "EmissionRecord", "ScopeClassification", "ProductFootprint"],
        "energy_management/models.py": ["Site", "Meter", "MeterReading", "TariffPlan", "UtilityBill", "RenewableAsset", "BatteryAsset"],
        "decarbonization/models.py": ["DecarbonizationProject", "ProjectMilestone", "ProjectAbatement", "EmissionTarget", "ScenarioRun"],
        "supplier_intelligence/models.py": ["Supplier", "SupplierDisclosure", "SupplierScorecard", "SupplierCategory", "SupplierBenchmark"],
        "audits_actions/models.py": ["Audit", "AuditFinding", "CorrectiveAction", "ActionComment", "ActionEvidence"],
        "analytics/models.py": ["KPIDefinition", "KPIResult", "MaterializedViewRefreshLog", "ForecastRun", "AnomalyEvent"],
        "reporting/models.py": ["ReportTemplate", "ReportRun", "ReportRecipient", "ExportJob"],
    }

    for rel_path, names in expected.items():
        source = (BLUEPRINT_APPS / rel_path).read_text()
        for name in names:
            assert f"class {name}(" in source
