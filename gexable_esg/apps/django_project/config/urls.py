from django.contrib import admin
from django.urls import include, path

from core_api import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ui/data-intake", views.ui_data_intake, name="ui-data-intake"),
    path("ui/emissions", views.ui_emissions, name="ui-emissions"),
    path("ui/disclosures", views.ui_disclosures, name="ui-disclosures"),
    path("ui/events", views.ui_events, name="ui-events"),
    path("ui/health", views.ui_health, name="ui-health"),
    path("ui/admin-portal", views.ui_admin_portal, name="ui-admin-portal"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("core_api.urls")),
    path("api/auth/", include("apps.users.urls")),
    path("api/tenants/", include("apps.tenants.urls")),
    path("api/dashboard/", include("apps.dashboard_api.urls")),
    path("api/emissions/", include("apps.emissions_management.urls")),
    path("api/", include("apps.energy_management.urls")),
    path("api/", include("apps.supplier_intelligence.urls")),
    path("api/", include("apps.decarbonization.urls")),
    path("api/", include("apps.audits_actions.urls")),
    path("api/", include("apps.data_ingestion.urls")),
    path("api/reporting/", include("apps.reporting.urls")),
]
