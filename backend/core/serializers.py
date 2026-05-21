from rest_framework import serializers

from . import models

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = models.CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'phone_number',
            'email',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password does not match!"})
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = models.CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class ServiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service

        fields = [
            'id',
            'title',
            'duration',
            'reserve_fee',
            'svg',
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

class ServiceSerializer(serializers.SerializerMethodField):
    class Meta:
        model = models.Service
        fields = [
            'id',
            'title',
            'duration',
            'reserve_fee',
            'svg',

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

class SlotSerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    is_available = serializers.BooleanField()