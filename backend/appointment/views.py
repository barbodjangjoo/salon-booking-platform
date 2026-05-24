from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from . import models
from . import serializers

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_appointment_view(request):
    serializer = serializers.AppointmentSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    appointment = serializer.save(customer=request.user)



    return Response({
        'detail': ('Appointment created successfully!'),
    },
    status=status.HTTP_200_OK
    )
