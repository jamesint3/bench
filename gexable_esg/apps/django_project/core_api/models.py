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


class BusinessUnit(TenantStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="business_units")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=80)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    class Meta:
        unique_together = ("tenant_id", "code")


class Asset(TenantStampedModel):
    STATUS_ACTIVE = "active"
    STATUS_RETIRED = "retired"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_RETIRED, "Retired"),
    ]

    site = models.ForeignKey(Site, on_delete=models.PROTECT, related_name="assets")
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name="assets")
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=100)
    external_id = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    commissioned_on = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("tenant_id", "external_id")


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
    version = models.CharField(max_length=50, default="v1")


class EmissionResult(TenantStampedModel):
    activity_record = models.ForeignKey(ActivityRecord, on_delete=models.PROTECT, related_name="emission_results")
    scope = models.CharField(max_length=20)
    co2e_kg = models.DecimalField(max_digits=16, decimal_places=4)
    calculation_method_version = models.CharField(max_length=50, default="v1")
    factor_version = models.CharField(max_length=50, default="v1")


class DisclosureReport(TenantStampedModel):
    STATUS_DRAFT = "draft"
    STATUS_IN_REVIEW = "in_review"
    STATUS_APPROVED = "approved"
    STATUS_PUBLISHED = "published"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_IN_REVIEW, "In review"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_PUBLISHED, "Published"),
    ]

    framework = models.CharField(max_length=30)
    period = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default=STATUS_DRAFT, choices=STATUS_CHOICES)


class Control(TenantStampedModel):
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_INACTIVE, "Inactive"),
    ]

    FREQ_AD_HOC = "ad_hoc"
    FREQ_MONTHLY = "monthly"
    FREQ_QUARTERLY = "quarterly"
    FREQ_ANNUAL = "annual"

    FREQUENCY_CHOICES = [
        (FREQ_AD_HOC, "Ad hoc"),
        (FREQ_MONTHLY, "Monthly"),
        (FREQ_QUARTERLY, "Quarterly"),
        (FREQ_ANNUAL, "Annual"),
    ]

    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name="controls")
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default=FREQ_MONTHLY)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    class Meta:
        unique_together = ("tenant_id", "code")


class DisclosureMetric(TenantStampedModel):
    report = models.ForeignKey(DisclosureReport, on_delete=models.CASCADE, related_name="metrics")
    metric_code = models.CharField(max_length=100)
    metric_name = models.CharField(max_length=255)
    metric_value = models.DecimalField(max_digits=18, decimal_places=6)
    unit = models.CharField(max_length=30)


class EvidenceFile(TenantStampedModel):
    report = models.ForeignKey(DisclosureReport, on_delete=models.CASCADE, related_name="evidence_files")
    file_name = models.CharField(max_length=255)
    file_uri = models.TextField()
    source_ref = models.CharField(max_length=120, blank=True, default="")


class Approval(TenantStampedModel):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    report = models.ForeignKey(DisclosureReport, on_delete=models.CASCADE, related_name="approvals")
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requested_approvals",
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="decided_approvals",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    decided_at = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True, default="")


class Target(TenantStampedModel):
    STATUS_ACTIVE = "active"
    STATUS_SUPERSEDED = "superseded"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_SUPERSEDED, "Superseded"),
        (STATUS_COMPLETED, "Completed"),
    ]

    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name="targets")
    scope = models.CharField(max_length=20)
    metric = models.CharField(max_length=80, default="co2e_kg")
    baseline_year = models.PositiveIntegerField()
    baseline_value = models.DecimalField(max_digits=18, decimal_places=6)
    target_year = models.PositiveIntegerField()
    target_value = models.DecimalField(max_digits=18, decimal_places=6)
    unit = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)


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
