from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from . import models

@api_view(["GET"])
def category_list_view(request):
    qs = models.Category.objects.all()
    serializer = serializers.CategorySerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def category_detail_view(request, pk):
    category = get_object_or_404(models.Category, pk=pk)
    serializer = serializers.CategorySerializer(category)
    return Response(serializer.data)


@api_view(["GET"])
def service_list_view(request, pk):
    service = get_object_or_404(
        models.Service.objects.prefetch_related('staff'), 
        pk=pk)
    print(service)
    serializer = serializers.ServiceSerializer(service)
    return Response(serializer.data)

@api_view(['GET'])
def staff_list_view(request, pk):
    staff = get_object_or_404(
        models.Staff.objects.prefetch_related('slot_set'), 
        pk=pk
        )

    serializer = serializers.StaffWithSlotSerializer(staff)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):
    user = request.user

    qs = models.Appointment.objects.filter(customer=user)
    serializer = serializers.AppointmentSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes(['GET'])
def appointment_detail_view(request, pk):
    appointment = get_object_or_404(models.Appointment, pk=pk)
    serializer = serializers.AppointmentSerializer(appointment)
    return Response(serializer.data)

@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def appointment_create_view(request):
    data = 
