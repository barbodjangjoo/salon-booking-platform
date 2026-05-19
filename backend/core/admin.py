from django.contrib import admin

from . import models

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    resource_class = models.CustomUser
    list_display = [
        'id',
        'first_name',
        'last_name',
        'phone_number',
        'is_phone_verified'
    ]

@admin.register(models.Services)
class AdminServices(admin.ModelAdmin):
    resource_class = models.Services
    list_display = [
        'id',
        'title',
        'requirement_time',
        'duration',
        'reserve_fee'
    ]

@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    resource_class = models.Staff
    fields = [
        'user',
        'service'
    ]

@admin.register(models.Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    resource_class = models.Availability
    fields = [
        'id',
        'staff',
        'date',
        'start_time',
        'end_time',
        'is_active'
    ]
    list_filter = ['date', 'is_active']
    search_fields = ['staff__user__first_name']
