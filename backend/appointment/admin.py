from django.contrib import admin

from . import models

@admin.register(models.Slot)
class SlotAdmin(admin.ModelAdmin):
    resource_class = models.Slot
    fields = [
        'id',
        'staff',
        'availability',
        'date',
        'start_time',
        'end_time',
        'status',
    ]

@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    resource_class = models.Appointment
    fields = [
        'customer',
        'staff',
        'booking_source',
    ]
    autocomplete_fields = ['customer', 'staff']