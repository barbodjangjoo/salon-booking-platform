from rest_framework import serializers

from . import models

class ServiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service

        fields = [
            'id',
            'title',
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
            'service'
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