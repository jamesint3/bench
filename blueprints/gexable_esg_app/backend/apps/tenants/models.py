from django.db import models

from apps.core.constants import RecordStatus, SubscriptionTier
from apps.core.models import TenantStampedModel, TimeStampedMixin


class Tenant(TimeStampedMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    industry = models.CharField(max_length=120, blank=True, default="")
    country = models.CharField(max_length=2)
    timezone = models.CharField(max_length=80, default="UTC")
    subscription_tier = models.CharField(max_length=20, choices=SubscriptionTier.choices, default=SubscriptionTier.STARTER)
    status = models.CharField(max_length=20, choices=RecordStatus.choices, default=RecordStatus.ACTIVE)

    def __str__(self) -> str:
        return self.name


class TenantSettings(TimeStampedMixin):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="settings")
    brand_name = models.CharField(max_length=255, blank=True, default="")
    primary_color = models.CharField(max_length=20, blank=True, default="#1F2937")
    secondary_color = models.CharField(max_length=20, blank=True, default="#4B5563")
    logo_url = models.URLField(blank=True, default="")
    locale = models.CharField(max_length=20, default="en")


class TenantFeatureFlag(TenantStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="feature_flags")
    key = models.CharField(max_length=100)
    enabled = models.BooleanField(default=False)
    rollout_percentage = models.PositiveSmallIntegerField(default=100)

    class Meta:
        unique_together = ("tenant", "key")
