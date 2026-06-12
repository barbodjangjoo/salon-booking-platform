from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from . import models
from . import serializers
from salon import models as salon_models

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def factor_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Factor.objects
            .prefetch_related('items')
            .filter(user=request.user)
        )

        serializer = serializers.FactorSerializer(qs, many=True)
        return Response(serializer.data)

    data = serializers.AddPurchaseItem(data=request.data)
    data.is_valid(raise_exception=True)

    appointment = get_object_or_404(
        salon_models.Appointment,
        pk=data.validated_data['appointment_id']
    )

    if appointment.slot.status != 'available':
        return Response(
            {'detail': 'Slot is not available'},
            status=400
        )

    with transaction.atomic():

        factor = models.Factor.objects.create(
            user=request.user,
            payment_status='pending',
            total_price=appointment.service.reserve_fee,
        )

        models.PurchaseItem.objects.create(
            factor=factor,
            appointment=appointment,
            title='Appointment',
            unit_price=appointment.service.reserve_fee,
        )

        appointment.slot.status = 'reserved'
        appointment.slot.save(update_fields=['status'])

    serializer = serializers.FactorSerializer(factor)
    return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factor_detail_view(request, pk):
    factor = get_object_or_404(
        models.Factor.objects.prefetch_related('items'),
        pk=pk
        )
    serializer = serializers.FactorSerializer(factor)

    return Response(serializer.data)