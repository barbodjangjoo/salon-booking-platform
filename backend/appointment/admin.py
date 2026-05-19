from django.contrib import admin

from . import models

@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    resource_class = models.Appointment
    fields = [
        'id',
        'customer',
        'staff',
        'service',
        'date',
        'start_time',
        'end_time',
        'status'
    ]
    list_filter = ['status', 'date']
    autocomplete_fields = ['customer', 'staff', 'service']