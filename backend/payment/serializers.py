from rest_framework import serializers

from . import models

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseItem
        fields = [
            'id',
            'factor',
            'appointment',
            'title',
            'quantity',
            'unit_price',
            'total_price'
        ]

class FactorSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer()
    class Meta:
        model = models.Factor
        fields =[
            'id',
            'user',
            'payment_status',
            'total_price',
            'transaction_datetime',
            'items'
        ]


class AddPurchaseItem(serializers.Serializer):
    appointment_id = serializers.CharField()
