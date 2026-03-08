from django.db import models

from apps.core.models import TenantStampedModel


class SupplierCategory(TenantStampedModel):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")


class Supplier(TenantStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(SupplierCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="suppliers")
    country = models.CharField(max_length=2, blank=True, default="")
    industry = models.CharField(max_length=120, blank=True, default="")
    active_flag = models.BooleanField(default=True)


class SupplierDisclosure(TenantStampedModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="disclosures")
    period_start = models.DateField()
    period_end = models.DateField()
    emissions_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    data_quality_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)


class SupplierScorecard(TenantStampedModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="scorecards")
    period_start = models.DateField()
    period_end = models.DateField()
    score = models.DecimalField(max_digits=6, decimal_places=2)
    engagement_status = models.CharField(max_length=30, default="not_started")


class SupplierBenchmark(TenantStampedModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="benchmarks")
    period_start = models.DateField()
    period_end = models.DateField()
    emissions_intensity = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    peer_percentile = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
