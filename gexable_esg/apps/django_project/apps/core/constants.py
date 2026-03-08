from django.db import models


class SubscriptionTier(models.TextChoices):
    STARTER = "starter", "Starter"
    GROWTH = "growth", "Growth"
    ENTERPRISE = "enterprise", "Enterprise"


class RecordStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class JobStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    RUNNING = "running", "Running"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"


class ScopeType(models.TextChoices):
    SCOPE_1 = "scope_1", "Scope 1"
    SCOPE_2 = "scope_2", "Scope 2"
    SCOPE_3 = "scope_3", "Scope 3"
