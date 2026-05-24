from django.shortcuts import render
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
def appointment_view(request):
    qs = models.Appointment.objects.filter(customer = request.user).all()

    serializer = serializers.AppointmentListView(qs, many=True)

    return Response(serializer.data)
