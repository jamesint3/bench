from django.contrib import admin

from .models import (
    AnomalyEvent,
    FactEmissionsMonthly,
    FactEnergyConsumptionDaily,
    FactSupplierEmissions,
    FactTariffCosts,
    ForecastRun,
    KPIAuditActions,
    KPIEmissionsOverview,
    KPIEnergySiteMonthly,
    KPIRenewablePerformance,
    KPISupplierBenchmark,
    MaterializedViewRefreshLog,
)

admin.site.register(FactEnergyConsumptionDaily)
admin.site.register(FactEmissionsMonthly)
admin.site.register(FactSupplierEmissions)
admin.site.register(FactTariffCosts)
admin.site.register(KPIEmissionsOverview)
admin.site.register(KPIEnergySiteMonthly)
admin.site.register(KPIRenewablePerformance)
admin.site.register(KPISupplierBenchmark)
admin.site.register(KPIAuditActions)
admin.site.register(MaterializedViewRefreshLog)
admin.site.register(ForecastRun)
admin.site.register(AnomalyEvent)
