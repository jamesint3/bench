from django.contrib import admin

from .models import (
    ActivityRecord,
    AuditLog,
    DisclosureReport,
    DomainEventOutbox,
    EmissionFactor,
    EmissionResult,
    Organization,
    Site,
    UserRole,
)

admin.site.register(Organization)
admin.site.register(Site)
admin.site.register(ActivityRecord)
admin.site.register(EmissionFactor)
admin.site.register(EmissionResult)
admin.site.register(DisclosureReport)
admin.site.register(AuditLog)
admin.site.register(DomainEventOutbox)
admin.site.register(UserRole)
