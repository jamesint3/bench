from django.db import models

from apps.core.models import TenantStampedModel


class Audit(TenantStampedModel):
    site = models.ForeignKey("energy_management.Site", on_delete=models.CASCADE, related_name="audits")
    name = models.CharField(max_length=255)
    audit_type = models.CharField(max_length=80)
    audit_date = models.DateField()
    auditor_name = models.CharField(max_length=255)
    status = models.CharField(max_length=30, default="open")


class AuditFinding(TenantStampedModel):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name="findings")
    site = models.ForeignKey("energy_management.Site", on_delete=models.CASCADE)
    severity = models.CharField(max_length=30)
    category = models.CharField(max_length=120)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=30, default="open")
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL)


class CorrectiveAction(TenantStampedModel):
    finding = models.ForeignKey(AuditFinding, on_delete=models.CASCADE, related_name="actions")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=30, default="open")
    priority = models.CharField(max_length=30, default="medium")
    owner = models.ForeignKey("users.User", on_delete=models.PROTECT)
    due_date = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)


class ActionComment(TenantStampedModel):
    action = models.ForeignKey(CorrectiveAction, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("users.User", on_delete=models.PROTECT)
    comment = models.TextField()


class ActionEvidence(TenantStampedModel):
    action = models.ForeignKey(CorrectiveAction, on_delete=models.CASCADE, related_name="evidence")
    file_name = models.CharField(max_length=255)
    file_uri = models.TextField()
