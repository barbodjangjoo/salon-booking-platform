from datetime import datetime, timedelta

from appointment.models import Appointment


def generate_available_slots(
    availability,
    service
):

    slots = []

    service_duration = service.duration

    gap = (
        availability
        .staff
        .min_gap_between_appointments
    )

    current_datetime = datetime.combine(
        availability.date,
        availability.start_time
    )

    end_datetime = datetime.combine(
        availability.date,
        availability.end_time
    )

    reserved_appointments = Appointment.objects.filter(
        staff=availability.staff,
        date=availability.date,
        status__in=[
            'pending',
            'confirmed'
        ]
    )

    while True:

        slot_end_datetime = (
            current_datetime +
            timedelta(minutes=service_duration)
        )

        if slot_end_datetime > end_datetime:
            break

        is_reserved = reserved_appointments.filter(
            start_time=current_datetime.time()
        ).exists()

        slots.append({
            'start_time': current_datetime.time(),
            'end_time': slot_end_datetime.time(),
            'is_available': not is_reserved
        })

        current_datetime += timedelta(
            minutes=service_duration + gap
        )

    return slots