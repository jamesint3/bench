from django.db import models

from apps.core.models import TimeStampedMixin


class User(models.Model):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=150, blank=True, default="")
    last_name = models.CharField(max_length=150, blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    class Meta:
        db_table = "users"


class UserProfile(TimeStampedMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    job_title = models.CharField(max_length=120, blank=True, default="")
    department = models.CharField(max_length=120, blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")


class UserTenantMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenant_memberships")
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="user_memberships")
    role = models.ForeignKey("permissions.Role", on_delete=models.PROTECT, related_name="membership_links")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_tenant_memberships"
        unique_together = ("user", "tenant", "role")
