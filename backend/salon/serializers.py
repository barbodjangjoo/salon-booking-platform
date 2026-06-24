from rest_framework import serializers
from datetime import datetime
from django.utils import timezone

from . import models

class ServiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service

        fields = [
            'id',
            'title',
            'svg',
            'duration',
            'reserve_fee',
        ]

class CategorySerializer(serializers.ModelSerializer):
    services = ServiceListSerializer(many=True, read_only=True)
    class Meta:
        model = models.Category
        fields = [
            'id',
            'title',
            'svg',
            'services'
        ]


class StaffSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = models.Staff
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
        ]
class ServiceSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(many=True, read_only=True)
    class Meta:
        model = models.Service
        fields = [
            'id',
            'title',
            'duration',
            'reserve_fee',
            'staff',
        ]

class SlotSerializer(serializers.ModelSerializer):
    staff = StaffSerializer()
    status = serializers.SerializerMethodField()
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

    def get_status(self, obj):
        slot_datetime = timezone.make_aware(
            datetime.combine(
                obj.date.togregorian(),
                obj.start_time
            )
        )

        if slot_datetime <= timezone.now():
            return 'unavailable'

        return obj.status


class SlotDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slot
        fields = [
            'id',
            'date',
            'start_time',
            'end_time',
            'status'
        ]

class StaffWithSlotSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    slots = SlotDetailSerializer(many=True, read_only=True, source='slot_set')
    class Meta:
        model = models.Staff
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
            'slots'
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='staff.user.first_name')
    last_name = serializers.CharField(source= 'staff.user.last_name')
    service = serializers.CharField(source= 'service.title')
    slot = SlotDetailSerializer()
    class Meta:
        model = models.Appointment
        fields = [
            'id',
            'first_name',
            'last_name',
            'slot',
            'service',
            'booking_source'
        ]

class CreateAppointmentSerializer(serializers.Serializer):
    slot_id = serializers.IntegerField()
    service_id = serializers.IntegerField()

class AvailabilitySerializer(serializers.ModelSerializer):
    staff = StaffSerializer()
    class Meta:
        model = models.Availability
        fields = [
            'id',
            'staff',
            'date',
            'start_time',
            'end_time',
            'is_active'
        ]