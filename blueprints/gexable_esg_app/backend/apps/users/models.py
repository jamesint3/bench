from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TenantStampedModel, TimeStampedMixin


class User(AbstractUser):
    email = models.EmailField(unique=True)
    preferred_timezone = models.CharField(max_length=80, default="UTC")


class UserProfile(TimeStampedMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    job_title = models.CharField(max_length=120, blank=True, default="")
    department = models.CharField(max_length=120, blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")


class UserTenantMembership(TenantStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenant_memberships")
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="user_memberships")
    is_default = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        unique_together = ("user", "tenant")
