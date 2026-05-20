from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from . import serializers
from . import models


@api_view(['POST'])
def user_registration(request):
    serializer = serializers.RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    return Response({
        'user': serializer.data,
        'token': tokens,
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def category_list_view(request):
    qs = models.Category.objects.prefetch_related('services').all()
    serializer = serializers.CategorySerializer(qs, many=True)
    return Response(serializer.data)