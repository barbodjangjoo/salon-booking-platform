from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factor_list_view(request):
    user = request.user

    qs = models.Factor.objects.filter(user=user).all()
    serializer = serializers.FactorSerializer(qs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factor_detail_view(request, pk):
    factor = get_object_or_404(
        models.Factor.objects.prefetch_related('factors'),
        pk=pk
        )
    serializer = serializers.FactorSerializer(factor)

    return Response(serializer.data)