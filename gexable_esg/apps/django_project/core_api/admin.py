from django.contrib import admin

from .models import (
    Approval,
    ActivityRecord,
    Asset,
    AuditLog,
    BusinessUnit,
    Control,
    DisclosureReport,
    DisclosureMetric,
    DomainEventOutbox,
    EvidenceFile,
    EmissionFactor,
    EmissionResult,
    Organization,
    Site,
    Target,
    UserRole,
)

admin.site.register(Organization)
admin.site.register(Site)
admin.site.register(BusinessUnit)
admin.site.register(Asset)
admin.site.register(ActivityRecord)
admin.site.register(EmissionFactor)
admin.site.register(EmissionResult)
admin.site.register(DisclosureReport)
admin.site.register(DisclosureMetric)
admin.site.register(EvidenceFile)
admin.site.register(Control)
admin.site.register(Approval)
admin.site.register(Target)
admin.site.register(AuditLog)
admin.site.register(DomainEventOutbox)
admin.site.register(UserRole)
