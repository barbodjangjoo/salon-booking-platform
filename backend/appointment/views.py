from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from . import models
from . import serializers

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_appointment_view(request):
    serializer = serializers.AppointmentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    appointment = serializer.save(customer=request.user)



    return Response({
        'detail': ('Appointment created successfully!'),
    },
    status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):
    qs = models.Appointment.objects.filter(customer = request.user).all()

    serializer = serializers.AppointmentListView(qs, many=True)

    return Response(serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def appointment_detail_view(request, pk):
    appointment = get_object_or_404(
        models.Appointment, 
        pk=pk,
        customer = request.user
        )
    if request.method == 'GET':
        serializer = serializers.AppointmentListView(appointment)

    # elif request.method == 'PATCH':
    #     serializer = serializers.AppointmentSerializer(appointment, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data)
    
    elif request.method == 'DELETE':
        appointment.status = 'cancelled'
        appointment.save()
        return Response(
            {
                'detail': 'Your appointment has been canceled'
            }
        )

    return Response(serializer.data)