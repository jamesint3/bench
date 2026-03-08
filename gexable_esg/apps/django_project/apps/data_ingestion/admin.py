from django.contrib import admin

from .models import DataQualityScore, DataSource, ImportFile, ImportJob, ValidationIssue

admin.site.register(DataSource)
admin.site.register(ImportJob)
admin.site.register(ImportFile)
admin.site.register(ValidationIssue)
admin.site.register(DataQualityScore)
