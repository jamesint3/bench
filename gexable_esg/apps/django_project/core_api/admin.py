from django.contrib import admin

from .models import ActivityRecord, AuditLog, DisclosureReport, EmissionFactor, EmissionResult, Organization, Site

admin.site.register(Organization)
admin.site.register(Site)
admin.site.register(ActivityRecord)
admin.site.register(EmissionFactor)
admin.site.register(EmissionResult)
admin.site.register(DisclosureReport)
admin.site.register(AuditLog)
