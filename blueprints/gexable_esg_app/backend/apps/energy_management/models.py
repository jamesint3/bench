from django.db import models

from apps.core.models import TenantStampedModel


class Site(TenantStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=80)
    country = models.CharField(max_length=2)
    region = models.CharField(max_length=80, blank=True, default="")
    site_type = models.CharField(max_length=80, blank=True, default="")
    floor_area_m2 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    production_unit = models.CharField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        db_table = "sites"
        unique_together = ("tenant_id", "code")


class Meter(TenantStampedModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="meters")
    meter_name = models.CharField(max_length=255)
    meter_type = models.CharField(max_length=80)
    unit = models.CharField(max_length=30)
    interval_minutes = models.PositiveIntegerField(default=15)
    source_system = models.CharField(max_length=120, blank=True, default="")
    status = models.CharField(max_length=20, default="active")

    class Meta:
        db_table = "meters"


class MeterReading(TenantStampedModel):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name="readings")
    reading_timestamp = models.DateTimeField()
    value = models.DecimalField(max_digits=18, decimal_places=6)
    unit = models.CharField(max_length=30)
    quality_flag = models.CharField(max_length=20, blank=True, default="")
    source_file_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "meter_readings_raw"


class TariffPlan(TenantStampedModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="tariff_plans")
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, default="USD")
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)


class UtilityBill(TenantStampedModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="utility_bills")
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    utility_type = models.CharField(max_length=40)
    consumption = models.DecimalField(max_digits=18, decimal_places=6)
    consumption_unit = models.CharField(max_length=30)
    cost_amount = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    demand_charge = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    source_file_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "utility_bills_raw"


class RenewableAsset(TenantStampedModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="renewable_assets")
    asset_type = models.CharField(max_length=80)
    name = models.CharField(max_length=255)
    capacity_kw = models.DecimalField(max_digits=12, decimal_places=2)
    commission_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        db_table = "renewable_assets"


class BatteryAsset(TenantStampedModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="battery_assets")
    name = models.CharField(max_length=255)
    power_kw = models.DecimalField(max_digits=12, decimal_places=2)
    energy_kwh = models.DecimalField(max_digits=12, decimal_places=2)
    round_trip_efficiency = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        db_table = "battery_assets"
