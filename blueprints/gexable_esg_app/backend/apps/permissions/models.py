from django.db import models

from apps.core.models import TenantStampedModel


class Role(TenantStampedModel):
    tenant = models.ForeignKey("tenants.Tenant", null=True, blank=True, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True, default="")

    class Meta:
        db_table = "roles"
        unique_together = ("tenant", "name")


class Permission(TenantStampedModel):
    key = models.CharField(max_length=120, unique=True)
    module = models.CharField(max_length=40)
    action = models.CharField(max_length=40)
    scope = models.CharField(max_length=40, default="tenant")


class RolePermission(TenantStampedModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="permission_roles")

    class Meta:
        unique_together = ("role", "permission")


class UserRoleAssignment(TenantStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="role_assignments")
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="role_assignments")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_assignments")
    site = models.ForeignKey("energy_management.Site", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("user", "tenant", "role", "site")
