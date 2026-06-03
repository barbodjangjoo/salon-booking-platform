from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated


from . import serializers
from . import models


@api_view(["POST"])
def user_registration(request):
    serializer = serializers.RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    refresh = RefreshToken.for_user(user)
    tokens = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

    return Response(
        {
            "user": serializer.data,
            "token": tokens,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def user_view(request):
    user = request.user
    if request.method == "GET":
        serializer = serializers.CustomUserSerializer(user)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = serializers.CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
