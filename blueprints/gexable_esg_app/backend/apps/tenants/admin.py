from django.contrib import admin

from .models import Tenant, TenantFeatureFlag, TenantSettings

admin.site.register(Tenant)
admin.site.register(TenantSettings)
admin.site.register(TenantFeatureFlag)
