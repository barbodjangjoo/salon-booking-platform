from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
import jdatetime
from celery import shared_task

from .models import Availability, Slot


@shared_task
def generate_slots(availability_id):

    availability = (
        Availability.objects
        .select_related('staff')
        .get(id=availability_id)
    )

    if not availability.is_active:
        return

    staff = availability.staff

    service = staff.service.first()

    if not service:
        return

    duration = service.duration
    gap = staff.min_gap_between_appointments

    current_datetime = datetime.combine(
        availability.date.togregorian(),
        availability.start_time
    )

    end_datetime = datetime.combine(
        availability.date.togregorian(),
        availability.end_time
    )

    while True:

        slot_end = (
            current_datetime +
            timedelta(minutes=duration)
        )

        if slot_end > end_datetime:
            break

        Slot.objects.get_or_create(
            staff=staff,
            availability=availability,
            date=availability.date,
            start_time=current_datetime.time(),
            defaults={
                'end_time': slot_end.time(),
                'status': 'available'
            }
        )

        current_datetime += timedelta(
            minutes=duration + gap
        )



@shared_task
def block_expired_slots():
    
    now = timezone.localtime()

    today = jdatetime.date.today()
    current_time = now.time()

    expired_slots = Slot.objects.filter(
        status="available"
    ).filter(
        Q(date__lt=today) |
        Q(
            date=today,
            end_time__lt=current_time
        )
    )

    updated_count = expired_slots.update(
        status="blocked"
    )

    return f"{updated_count} slots blocked"