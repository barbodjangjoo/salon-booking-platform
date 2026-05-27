from django.contrib import admin
from django_jalali.admin.widgets import AdminjDateWidget


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
    search_fields = ['first_name', 'last_name', 'phone_number']

@admin.register(models.Service)
class AdminServices(admin.ModelAdmin):
    resource_class = models.Service
    list_display = [
        'id',
        'title',
        'requirement_time',
        'duration',
        'reserve_fee'
    ]
    search_fields = ['title']

@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    resource_class = models.Staff
    list_display = [
        'id',
        'user',
        'min_gap_between_appointments'
    ]
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(models.Availability)
class AvailabilityAdmin(
    admin.ModelAdmin
):
    resource_class = models.Availability

    list_display = [
        'id',
        'staff',
        'date',
        'start_time',
        'end_time',
        'is_active'
    ]

    list_filter = [
        ('date'),
        'is_active'
    ]

    search_fields = [
        'staff__user__first_name'
    ]
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    resource_class = models.Category
    list_display = ['id', 'title']
