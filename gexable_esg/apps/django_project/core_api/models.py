from django.conf import settings
from django.db import models

from .tenant import TenantScopedManager


class TenantStampedModel(models.Model):
    tenant_id = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TenantScopedManager()

    class Meta:
        abstract = True


class Organization(TenantStampedModel):
    name = models.CharField(max_length=255)


class Site(TenantStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="sites")
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2)


class ActivityRecord(TenantStampedModel):
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=16, decimal_places=4)
    unit = models.CharField(max_length=30, default="kWh")
    source_type = models.CharField(max_length=50, default="manual_upload")
    idempotency_key = models.CharField(max_length=120, unique=True)


class EmissionFactor(TenantStampedModel):
    code = models.CharField(max_length=100)
    unit = models.CharField(max_length=30)
    co2e_per_unit = models.DecimalField(max_digits=16, decimal_places=8)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=255, default="internal")


class EmissionResult(TenantStampedModel):
    activity_record = models.ForeignKey(ActivityRecord, on_delete=models.PROTECT, related_name="emission_results")
    scope = models.CharField(max_length=20)
    co2e_kg = models.DecimalField(max_digits=16, decimal_places=4)
    calculation_method_version = models.CharField(max_length=50, default="v1")
    factor_version = models.CharField(max_length=50, default="v1")


class DisclosureReport(TenantStampedModel):
    framework = models.CharField(max_length=30)
    period = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="draft")


class AuditLog(TenantStampedModel):
    action = models.CharField(max_length=80)
    entity_type = models.CharField(max_length=80)
    entity_id = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)


class DomainEventOutbox(TenantStampedModel):
    topic = models.CharField(max_length=120)
    payload = models.JSONField(default=dict)
    schema_version = models.CharField(max_length=20, default="v1")
    status = models.CharField(max_length=20, default="pending", db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)


class UserRole(TenantStampedModel):
    ROLE_PREPARER = "preparer"
    ROLE_REVIEWER = "reviewer"
    ROLE_APPROVER = "approver"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_PREPARER, "Preparer"),
        (ROLE_REVIEWER, "Reviewer"),
        (ROLE_APPROVER, "Approver"),
        (ROLE_ADMIN, "Admin"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gexable_roles")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("tenant_id", "user", "role")
