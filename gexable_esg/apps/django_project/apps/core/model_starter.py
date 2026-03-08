"""Starter model examples for first core tables (blueprint only).

These examples are intentionally isolated from the active runtime app.
"""

from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    industry = models.CharField(max_length=120, blank=True, default="")
    country = models.CharField(max_length=2, blank=True, default="")
    timezone = models.CharField(max_length=80, default="UTC")
    status = models.CharField(max_length=30, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Role(models.Model):
    tenant = models.ForeignKey(Tenant, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True, default="")


class Site(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=80)
    country = models.CharField(max_length=2)
    region = models.CharField(max_length=80, blank=True, default="")
    site_type = models.CharField(max_length=50, blank=True, default="")
    status = models.CharField(max_length=20, default="active")


class Meter(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    meter_name = models.CharField(max_length=255)
    meter_type = models.CharField(max_length=80)
    unit = models.CharField(max_length=30)
    interval_minutes = models.PositiveIntegerField(default=15)
    status = models.CharField(max_length=20, default="active")
