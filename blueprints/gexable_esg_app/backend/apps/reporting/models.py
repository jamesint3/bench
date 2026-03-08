from django.db import models

from apps.core.models import TenantStampedModel


class ReportTemplate(TenantStampedModel):
    name = models.CharField(max_length=255)
    framework = models.CharField(max_length=80)
    file_format = models.CharField(max_length=20, default="pdf")
    template_config = models.JSONField(default=dict)


class ReportRun(TenantStampedModel):
    template = models.ForeignKey(ReportTemplate, on_delete=models.PROTECT, related_name="runs")
    requested_by = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default="pending")
    output_uri = models.TextField(blank=True, default="")
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class ReportRecipient(TenantStampedModel):
    report_run = models.ForeignKey(ReportRun, on_delete=models.CASCADE, related_name="recipients")
    email = models.EmailField()
    delivery_status = models.CharField(max_length=20, default="pending")


class ExportJob(TenantStampedModel):
    report_run = models.ForeignKey(ReportRun, on_delete=models.CASCADE, related_name="exports")
    export_type = models.CharField(max_length=20, default="csv")
    status = models.CharField(max_length=20, default="pending")
    artifact_uri = models.TextField(blank=True, default="")
