from django.db import transaction
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Prefetch
from rest_framework.exceptions import ValidationError
import jdatetime
from django.db.models import Q

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

@api_view(['GET'])
def availablity_list_view(request):

    qs = models.Availability.objects.select_related(
        'staff__user'
        ).all()
    serializer = serializers.AvailabilitySerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def availablity_detail_view(request, pk):
    
    available = get_object_or_404(
        models.Availability.objects.select_related(
            'staff__user'
        ),
        pk=pk
    )
    serializer = serializers.AvailabilitySerializer(available)
    return Response(serializer.data)


@api_view(['GET'])
def slot_list_view(request, pk):

    today = jdatetime.date.today()
    current_time = timezone.localtime().time()
    
    qs = models.Slot.objects.select_related(
        'staff__user',
        'availability'
    ).filter(staff_id=pk).filter(
        Q(date__gt=today) |
        Q(date=today, start_time__gt = current_time )
    ).all()

    serializer = serializers.SlotSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def slot_detail_view(request, pk):
    
    today = jdatetime.date.today()
    
    slot = get_object_or_404(
        models.Slot.objects.select_related(
        'staff__user',
        'availability'
    ).filter(date__gt=today),
    pk=pk
    )
    serializer = serializers.SlotSerializer(slot)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):


    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            # چک زمان گذشته
            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)@api_view(['GET', 'POST'])
    

@permission_classes([IsAuthenticated])
def appointment_list_view(request):

    if request.method == 'GET':
        qs = (
            models.Appointment.objects
            .select_related(
                'customer',
                'staff__user',
                'slot',
                'service',
            )
            .filter(customer=request.user)
        )

        serializer = serializers.AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        data = serializers.CreateAppointmentSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        with Transaction.atomic():

            slot = get_object_or_404(
                models.Slot.objects.select_for_update(),
                pk=data.validated_data['slot_id']
            )

            service = get_object_or_404(
                models.Service,
                pk=data.validated_data['service_id']
            )

            if slot.status != 'available':
                raise ValidationError(
                    {'slot': 'This slot is not available.'}
                )

            if not slot.staff.service.filter(pk=service.pk).exists():
                raise ValidationError(
                    {'service': 'This staff does not provide this service.'}
                )

            today = timezone.localdate()
            now_time = timezone.localtime().time()

            if slot.date == today and slot.start_time <= now_time:
                raise ValidationError(
                    {'slot': 'This slot time has already passed.'}
                )

            appointment = models.Appointment.objects.create(
                customer=request.user,
                staff=slot.staff,
                slot=slot,
                service=service,
                booking_source='online'
            )

            slot.status = 'reserved'
            slot.save(update_fields=['status'])

        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=201)
