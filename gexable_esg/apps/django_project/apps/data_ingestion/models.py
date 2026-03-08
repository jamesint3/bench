from django.db import models

from apps.core.constants import JobStatus
from apps.core.models import TenantStampedModel


class DataSource(TenantStampedModel):
    SOURCE_TYPE_CHOICES = [("csv", "CSV"), ("excel", "Excel"), ("api", "API")]
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)
    connection_ref = models.CharField(max_length=255, blank=True, default="")


class ImportJob(TenantStampedModel):
    source = models.ForeignKey(DataSource, on_delete=models.PROTECT, related_name="jobs")
    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.PENDING)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    row_count = models.PositiveIntegerField(default=0)


class ImportFile(TenantStampedModel):
    import_job = models.ForeignKey(ImportJob, on_delete=models.CASCADE, related_name="files")
    file_name = models.CharField(max_length=255)
    file_uri = models.TextField()
    checksum = models.CharField(max_length=120, blank=True, default="")


class ValidationIssue(TenantStampedModel):
    import_job = models.ForeignKey(ImportJob, on_delete=models.CASCADE, related_name="validation_issues")
    severity = models.CharField(max_length=20, default="error")
    row_number = models.PositiveIntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=120, blank=True, default="")
    message = models.TextField()


class DataQualityScore(TenantStampedModel):
    import_job = models.OneToOneField(ImportJob, on_delete=models.CASCADE, related_name="quality_score")
    completeness_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    validity_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    uniqueness_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    overall_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
