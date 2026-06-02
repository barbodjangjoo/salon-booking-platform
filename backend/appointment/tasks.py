# appointment/tasks.py

from datetime import datetime, timedelta

from celery import shared_task

from core.models import Availability
from appointment.models import Slot


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