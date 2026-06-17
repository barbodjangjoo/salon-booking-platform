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
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'email',
        ]