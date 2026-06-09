from rest_framework import serializers

from . import models

class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Factor
        fields =[
            'id',
            'user',
            'payment_status',
            'datetime_transaction',
            'total_price',
        ]

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseItem
        fields = [
            'id',
            'user',
            'factor',
            'service',
            'price',
            'payment_status'
        ]