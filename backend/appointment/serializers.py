from rest_framework import serializers

from . import models

class AppointmentSerializers(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    end_time = serializers.DateField(read_only=True)
    class Meta:
        model = models.Appointment
        fields = [
            'id',
            'staff',
            'service',
            'date',
            'start_time',
            'end_time',
            'status',
        ]