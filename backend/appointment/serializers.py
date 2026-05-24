from rest_framework import serializers
from datetime import datetime, timedelta

from . import models
from core import models as coremodel
from core.services.booking import generate_available_slots

class AppointmentSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    end_time = serializers.TimeField(read_only=True)
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

    
    def validate(self, attrs):

        staff = attrs['staff']

        service = attrs['service']

        date = attrs['date']

        start_time = attrs['start_time']


        if not staff.service.filter(
            id=service.id
        ).exists():

            raise serializers.ValidationError(
                'This staff does not provide this service.'
            )

        availability = coremodel.Availability.objects.filter(
            staff=staff,
            date=date,
            is_active=True
        ).first()

        if not availability:

            raise serializers.ValidationError(
                'No availability found.'
            )
        
        slots = generate_available_slots(
            availability=availability,
            service=service
        )

        selected_slot = None

        for slot in slots:
            if slot['start_time'] == start_time:
                selected_slot = slot
                break

        if not selected_slot['is_available']:

            raise serializers.ValidationError(
                'This slot is already reserved.'
            )
        
        start_datetime = datetime.combine(
            date,
            start_time
        )

        end_datetime = (
            start_datetime +
            timedelta(
                minutes=service.duration
            )
        )

        attrs['end_time'] = end_datetime.time()

        return attrs
    
class AppointmentListView(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
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