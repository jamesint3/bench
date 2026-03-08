from django.contrib import admin

from .models import EmissionFactor, EmissionRecord, EmissionSource, ProductFootprint, ScopeClassification

admin.site.register(ScopeClassification)
admin.site.register(EmissionSource)
admin.site.register(EmissionFactor)
admin.site.register(EmissionRecord)
admin.site.register(ProductFootprint)
