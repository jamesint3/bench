from django.db import models

from apps.core.models import TenantStampedModel


class KPIDefinition(TenantStampedModel):
    code = models.CharField(max_length=120)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    query_config = models.JSONField(default=dict)

    class Meta:
        unique_together = ("tenant_id", "code")


class KPIResult(TenantStampedModel):
    kpi = models.ForeignKey(KPIDefinition, on_delete=models.CASCADE, related_name="results")
    period_start = models.DateField()
    period_end = models.DateField()
    value = models.DecimalField(max_digits=18, decimal_places=6)
    dimensions = models.JSONField(default=dict)


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
