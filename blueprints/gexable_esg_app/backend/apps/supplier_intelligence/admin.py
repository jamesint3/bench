from django.contrib import admin

from .models import Supplier, SupplierActivityRaw, SupplierBenchmark, SupplierCategory, SupplierDisclosure, SupplierScorecard

admin.site.register(SupplierCategory)
admin.site.register(Supplier)
admin.site.register(SupplierActivityRaw)
admin.site.register(SupplierDisclosure)
admin.site.register(SupplierScorecard)
admin.site.register(SupplierBenchmark)
