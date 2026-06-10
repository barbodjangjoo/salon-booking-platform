from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Prefetch

from . import serializers
from . import models

@api_view(["GET"])
def category_list_view(request):
    qs = models.Category.objects.prefetch_related('services').all()
    serializer = serializers.CategorySerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def category_detail_view(request, pk):
    category = get_object_or_404(models.Category, pk=pk)
    serializer = serializers.CategorySerializer(category)
    return Response(serializer.data)


@api_view(['GET'])
def service_list_view(request):
    qs = models.Service.objects.all()
    serializer = serializers.ServiceListSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def service_detail_view(request, pk):
    
    service = get_object_or_404(
        models.Service.objects.prefetch_related(
            Prefetch(
                'staff',
                queryset=models.Staff.objects.select_related('user')
            )),
        pk=pk
        )
    
    serializer = serializers.ServiceSerializer(service)
    return Response(serializer.data)

@api_view(['GET'])
def staff_list_view(request):
    
    qs = models.Staff.objects.select_related('user').only(
        'id',
        'user__first_name',
        'user__last_name',
    ).all()
    serializer = serializers.StaffSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def staff_detail_view(request, pk):

    staff = get_object_or_404(
        models.Staff.objects
        .select_related('user')
        .prefetch_related(
            'slot_set'
        ),
        pk=pk
    )

    serializer = serializers.StaffWithSlotSerializer(staff)
    return Response(serializer.data)