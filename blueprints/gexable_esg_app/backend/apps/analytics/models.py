from django.db import models

from apps.core.constants import ScopeType
from apps.core.models import TenantStampedModel


class FactEnergyConsumptionDaily(TenantStampedModel):
    site = models.ForeignKey("energy_management.Site", on_delete=models.CASCADE)
    date = models.DateField()
    energy_kwh = models.DecimalField(max_digits=18, decimal_places=6)
    peak_kw = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    offpeak_kwh = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    renewable_kwh = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    grid_import_kwh = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    grid_export_kwh = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    cost_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        db_table = "fact_energy_consumption_daily"


class FactEmissionsMonthly(TenantStampedModel):
    site = models.ForeignKey("energy_management.Site", null=True, blank=True, on_delete=models.SET_NULL)
    supplier = models.ForeignKey("supplier_intelligence.Supplier", null=True, blank=True, on_delete=models.SET_NULL)
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()
    scope = models.CharField(max_length=20, choices=ScopeType.choices)
    category = models.CharField(max_length=120)
    activity_amount = models.DecimalField(max_digits=18, decimal_places=6)
    activity_unit = models.CharField(max_length=30)
    emissions_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    methodology = models.CharField(max_length=120)
    factor_version = models.CharField(max_length=50)

    class Meta:
        db_table = "fact_emissions_monthly"


class FactSupplierEmissions(TenantStampedModel):
    supplier = models.ForeignKey("supplier_intelligence.Supplier", on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    scope3_category = models.CharField(max_length=120)
    emissions_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    data_quality_score = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_flag = models.BooleanField(default=False)

    class Meta:
        db_table = "fact_supplier_emissions"


class FactTariffCosts(TenantStampedModel):
    site = models.ForeignKey("energy_management.Site", on_delete=models.CASCADE)
    date = models.DateField()
    energy_charge = models.DecimalField(max_digits=18, decimal_places=2)
    demand_charge = models.DecimalField(max_digits=18, decimal_places=2)
    fixed_charge = models.DecimalField(max_digits=18, decimal_places=2)
    other_charge = models.DecimalField(max_digits=18, decimal_places=2)
    total_cost = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3)

    class Meta:
        db_table = "fact_tariff_costs"


class KPIEmissionsOverview(TenantStampedModel):
    period_type = models.CharField(max_length=20)
    period_value = models.CharField(max_length=30)
    total_scope1_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    total_scope2_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    total_scope3_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    total_emissions_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    target_emissions_tco2e = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    variance_tco2e = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    last_refreshed_at = models.DateTimeField()

    class Meta:
        db_table = "kpi_emissions_overview"


class KPIEnergySiteMonthly(TenantStampedModel):
    site = models.ForeignKey("energy_management.Site", on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()
    energy_kwh = models.DecimalField(max_digits=18, decimal_places=6)
    cost_amount = models.DecimalField(max_digits=18, decimal_places=2)
    energy_intensity = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    peak_kw = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    renewable_share_pct = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    last_refreshed_at = models.DateTimeField()

    class Meta:
        db_table = "kpi_energy_site_monthly"


class KPIRenewablePerformance(TenantStampedModel):
    site = models.ForeignKey("energy_management.Site", on_delete=models.CASCADE)
    asset = models.ForeignKey("energy_management.RenewableAsset", on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()
    generation_kwh = models.DecimalField(max_digits=18, decimal_places=6)
    self_consumption_pct = models.DecimalField(max_digits=6, decimal_places=2)
    export_kwh = models.DecimalField(max_digits=18, decimal_places=6)
    curtailment_kwh = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    availability_pct = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "kpi_renewable_performance"


class KPISupplierBenchmark(TenantStampedModel):
    supplier = models.ForeignKey("supplier_intelligence.Supplier", on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    emissions_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    emissions_intensity = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    data_quality_score = models.DecimalField(max_digits=6, decimal_places=2)
    peer_percentile = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    engagement_status = models.CharField(max_length=30)

    class Meta:
        db_table = "kpi_supplier_benchmark"


class KPIAuditActions(TenantStampedModel):
    site = models.ForeignKey("energy_management.Site", null=True, blank=True, on_delete=models.SET_NULL)
    period_start = models.DateField()
    period_end = models.DateField()
    open_findings = models.PositiveIntegerField()
    closed_findings = models.PositiveIntegerField()
    overdue_actions = models.PositiveIntegerField()
    closure_rate_pct = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = "kpi_audit_actions"


class MaterializedViewRefreshLog(TenantStampedModel):
    view_name = models.CharField(max_length=255)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="running")
    detail = models.TextField(blank=True, default="")


class ForecastRun(TenantStampedModel):
    model_name = models.CharField(max_length=120)
    period_start = models.DateField()
    period_end = models.DateField()
    metrics = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now_add=True)


class AnomalyEvent(TenantStampedModel):
    source = models.CharField(max_length=120)
    detected_at = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=20, default="medium")
    context = models.JSONField(default=dict)
