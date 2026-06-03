from django.contrib import admin

from . import models
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    resource_class = models.Category
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']


@admin.register(models.Service)
class AdminServices(admin.ModelAdmin):
    resource_class = models.Service
    list_display = [
        'id',
        'title',
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
    list_display_links = ['id', 'user']

@admin.register(models.Availability)
class AvailabilityAdmin(admin.ModelAdmin):
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

@admin.register(models.Slot)
class SlotAdmin(admin.ModelAdmin):
    resource_class = models.Slot
    list_display = (
        "staff",
        "date",
        "start_time",
        "end_time",
        "status",
    )

@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    resource_class = models.Appointment
    fields = [
        'customer',
        'staff',
        'booking_source',
    ]
    autocomplete_fields = ['customer', 'staff']