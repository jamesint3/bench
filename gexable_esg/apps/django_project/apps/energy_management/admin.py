from django.contrib import admin

from .models import BatteryAsset, Meter, MeterReading, RenewableAsset, Site, TariffPlan, UtilityBill

admin.site.register(Site)
admin.site.register(Meter)
admin.site.register(MeterReading)
admin.site.register(TariffPlan)
admin.site.register(UtilityBill)
admin.site.register(RenewableAsset)
admin.site.register(BatteryAsset)
