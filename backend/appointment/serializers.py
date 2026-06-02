from rest_framework import serializers

from . import models

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slot
        fields = [
            'id',
            'staff',
            'availability',
            'date',
            'start_time',
            'end_time',
            'status'
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = [
            'id',
            'staff',
            'slot',
            'service',
            'booking_source'
        ]