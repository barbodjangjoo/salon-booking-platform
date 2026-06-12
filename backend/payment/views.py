from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def factor_list_view(request):
    user = request.user
    if request.method == 'GET':
        qs = models.Factor.objects.filter(user=user).all()
        serializer = serializers.FactorSerializer(qs, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = serializers.AddPurchaseItem(data=request.data)
        data.is_valid(raise_exception=True)
        
        appoitment = get_object_or_404(models.Appointment, id=data.validated_data['id'])
        if appoitment:
            factor = models.Factor.objects.create(
                user = user,
                payment_status = 'pending',
                total_price = appoitment.service.reserve_fee,
            )
            models.PurchaseItem.objects.create(
                factor = factor,
                appointment=appoitment,
                title = 'Appointment',
                unit_price = factor.total_price,
                total_price = factor.total_price
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factor_detail_view(request, pk):
    factor = get_object_or_404(
        models.Factor.objects.prefetch_related('factors'),
        pk=pk
        )
    serializer = serializers.FactorSerializer(factor)

    return Response(serializer.data)