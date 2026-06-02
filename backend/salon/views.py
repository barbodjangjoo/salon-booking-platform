from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
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
    pass

