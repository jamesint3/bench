from django.db import models

from apps.core.constants import ScopeType
from apps.core.models import TenantStampedModel


class ScopeClassification(TenantStampedModel):
    code = models.CharField(max_length=50, choices=ScopeType.choices)
    category = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")


class EmissionSource(TenantStampedModel):
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=100)
    scope_classification = models.ForeignKey(ScopeClassification, on_delete=models.PROTECT, related_name="sources")


class EmissionFactor(TenantStampedModel):
    factor_code = models.CharField(max_length=120)
    scope = models.CharField(max_length=20, choices=ScopeType.choices)
    category = models.CharField(max_length=120)
    region = models.CharField(max_length=80)
    unit_from = models.CharField(max_length=30)
    unit_to = models.CharField(max_length=30, default="tco2e")
    factor_value = models.DecimalField(max_digits=18, decimal_places=8)
    factor_source = models.CharField(max_length=255, blank=True, default="")
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=50, default="v1")

    class Meta:
        db_table = "emission_factor_library"


class EmissionRecord(TenantStampedModel):
    source = models.ForeignKey(EmissionSource, on_delete=models.PROTECT, related_name="records")
    factor = models.ForeignKey(EmissionFactor, on_delete=models.PROTECT, related_name="records")
    activity_date = models.DateField()
    activity_amount = models.DecimalField(max_digits=18, decimal_places=6)
    activity_unit = models.CharField(max_length=30)
    emissions_tco2e = models.DecimalField(max_digits=18, decimal_places=6)


class ProductFootprint(TenantStampedModel):
    product_code = models.CharField(max_length=120)
    product_name = models.CharField(max_length=255)
    period_start = models.DateField()
    period_end = models.DateField()
    emissions_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    methodology = models.CharField(max_length=120, blank=True, default="")
