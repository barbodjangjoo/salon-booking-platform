from django.contrib import admin

from . import models

class PurchaseItemInline(admin.TabularInline):
    model = models.PurchaseItem
    extra = 0

@admin.register(models.Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_status']
    inlines = [PurchaseItemInline]