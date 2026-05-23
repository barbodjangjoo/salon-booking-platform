from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now


from . import serializers
from . import models
from .services.booking import generate_available_slots


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

@api_view(['GET'])
def services_detail_view(request, pk):
    service = get_object_or_404(models.Service, pk=pk)
    staff = models.Staff.objects.filter(service=service.id).select_related('user')
    serializer = serializers.StaffSerializer(staff, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def avaiable_slot_view(request, pk):

    service = get_object_or_404(
        models.Service,
        pk=pk
    )

    staff_id = request.GET.get('staff')

    staff = get_object_or_404(
        models.Staff,
        pk=staff_id
    )

    if not staff.service.filter(
        id=service.id
    ).exists():

        return Response({
            'detail': (
                'This staff does not provide this service!'
            )
        })

    availabilities = (
        models.Availability.objects.filter(
            staff=staff,
            is_active=True,
            date__gte=now().date()
        ).order_by('date')
    )

    all_slots = []

    for availability in availabilities:

        slots = generate_available_slots(
            availability=availability,
            service=service
        )

        all_slots.append({
            'date': availability.date,
            'slots': slots
        })

    serializer = serializers.AvailableSlotSerializer(
        all_slots,
        many=True
    )

    return Response(serializer.data)

