from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Warehouse)
admin.site.register(models.Item)
admin.site.register(models.Transfer)
admin.site.register(models.WarehouseProduct)
