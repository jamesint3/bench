from pathlib import Path


URLS_FILE = Path("gexable_esg/apps/django_project/config/urls.py")


def test_required_api_routes_wired_in_main_urls() -> None:
    source = URLS_FILE.read_text()
    assert 'path("api/auth/", include("apps.users.urls"))' in source
    assert 'path("api/tenants/", include("apps.tenants.urls"))' in source
    assert 'path("api/dashboard/", include("apps.dashboard_api.urls"))' in source
    assert 'path("api/emissions/", include("apps.emissions_management.urls"))' in source
    assert 'path("api/", include("apps.energy_management.urls"))' in source
    assert 'path("api/", include("apps.supplier_intelligence.urls"))' in source
    assert 'path("api/", include("apps.decarbonization.urls"))' in source
    assert 'path("api/", include("apps.audits_actions.urls"))' in source
    assert 'path("api/", include("apps.data_ingestion.urls"))' in source


def test_required_task_functions_exist() -> None:
    task_checks = {
        "gexable_esg/apps/django_project/apps/data_ingestion/tasks.py": [
            "def validate_import_file",
            "def process_meter_upload",
            "def process_supplier_upload",
        ],
        "gexable_esg/apps/django_project/apps/emissions_management/tasks.py": [
            "def calculate_scope1_emissions",
            "def calculate_scope2_emissions",
            "def calculate_scope3_emissions",
        ],
        "gexable_esg/apps/django_project/apps/energy_management/tasks.py": [
            "def aggregate_daily_energy",
            "def aggregate_monthly_energy",
            "def calculate_tariff_costs",
        ],
        "gexable_esg/apps/django_project/apps/analytics/tasks.py": [
            "def refresh_kpi_emissions_overview",
            "def refresh_kpi_energy_site_monthly",
            "def refresh_materialized_views",
            "def run_monthly_forecast",
            "def detect_energy_anomalies",
        ],
        "gexable_esg/apps/django_project/apps/reporting/tasks.py": ["def generate_scheduled_report"],
    }

    for file_path, signatures in task_checks.items():
        text = Path(file_path).read_text()
        for signature in signatures:
            assert signature in text


def test_frontend_structure_files_exist() -> None:
    expected_files = [
        "frontend/src/app/router.tsx",
        "frontend/src/app/providers.tsx",
        "frontend/src/app/auth.ts",
        "frontend/src/pages/DashboardHome.tsx",
        "frontend/src/pages/EmissionsOverviewPage.tsx",
        "frontend/src/pages/ScopeTrendsPage.tsx",
        "frontend/src/pages/EnergyBySitePage.tsx",
        "frontend/src/pages/TariffAnalysisPage.tsx",
        "frontend/src/pages/RenewablePerformancePage.tsx",
        "frontend/src/pages/DecarbonizationProjectsPage.tsx",
        "frontend/src/pages/SupplierBenchmarkingPage.tsx",
        "frontend/src/pages/AuditActionsPage.tsx",
        "frontend/src/tables/AGGridTable.tsx",
        "frontend/src/tables/DataTable.tsx",
        "frontend/src/charts/LineTrendChart.tsx",
        "frontend/src/charts/StackedBarChart.tsx",
        "frontend/src/charts/KPIStatCard.tsx",
        "frontend/src/charts/HeatmapChart.tsx",
        "frontend/src/services/api.ts",
        "frontend/src/services/dashboard.ts",
        "frontend/src/services/auth.ts",
        "frontend/src/services/exports.ts",
        "frontend/src/types/dashboard.ts",
        "frontend/src/types/emissions.ts",
        "frontend/src/types/energy.ts",
        "frontend/src/types/common.ts",
    ]
    for file_path in expected_files:
        assert Path(file_path).exists()


def test_frontend_routes_wired_in_main_urls() -> None:
    source = URLS_FILE.read_text()
    assert 'views.frontend_app' in source
    assert 'emissions-overview' in source
    assert 'demo/ui/data-intake' in source
