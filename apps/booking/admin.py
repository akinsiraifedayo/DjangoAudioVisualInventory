from django.contrib import admin
from . import models

# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    actions = ['duplicate_selected']

    def duplicate_selected(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # Set primary key to None to create a new object
            obj.save()

    duplicate_selected.short_description = "Duplicate selected %(verbose_name_plural)s"

class ClientAdmin(admin.ModelAdmin):
    actions = ['duplicate_selected']

    def duplicate_selected(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # Set primary key to None to create a new object
            obj.save()

    duplicate_selected.short_description = "Duplicate selected %(verbose_name_plural)s"


class EventAdmin(admin.ModelAdmin):
    list_display = ('name','status')



admin.site.register(models.Order)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.OrderItem)
admin.site.register(models.Invoice)
admin.site.register(models.PaymentAccount)


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Company, CompanyAdmin)