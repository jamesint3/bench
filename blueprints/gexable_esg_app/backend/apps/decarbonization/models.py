from django.db import models

from apps.core.models import TenantStampedModel


class DecarbonizationProject(TenantStampedModel):
    site = models.ForeignKey("energy_management.Site", null=True, blank=True, on_delete=models.SET_NULL, related_name="projects")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=80)
    status = models.CharField(max_length=30, default="planned")
    owner = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL)
    capex_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="USD")


class ProjectMilestone(TenantStampedModel):
    project = models.ForeignKey(DecarbonizationProject, on_delete=models.CASCADE, related_name="milestones")
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)


class ProjectAbatement(TenantStampedModel):
    project = models.ForeignKey(DecarbonizationProject, on_delete=models.CASCADE, related_name="abatements")
    period_start = models.DateField()
    period_end = models.DateField()
    expected_abatement_tco2e = models.DecimalField(max_digits=18, decimal_places=6)
    actual_abatement_tco2e = models.DecimalField(max_digits=18, decimal_places=6)


class EmissionTarget(TenantStampedModel):
    target_name = models.CharField(max_length=255)
    baseline_year = models.PositiveIntegerField()
    target_year = models.PositiveIntegerField()
    target_scope = models.CharField(max_length=40)
    target_reduction_pct = models.DecimalField(max_digits=6, decimal_places=2)
    science_based_flag = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default="active")


class ScenarioRun(TenantStampedModel):
    name = models.CharField(max_length=255)
    assumptions = models.JSONField(default=dict)
    run_at = models.DateTimeField(auto_now_add=True)
    result_summary = models.JSONField(default=dict)
