from datetime import datetime, timedelta

from appointment.models import Appointment

def generate_available_slots(availablity, service):

    slots = []

    service_duration = service.duration
    gap = availablity.staff.min_gap_between_appointments
    current_datetime = datetime.combine(
        availablity.data,
        availablity.start_time
    )

    end_datetime = datetime.combine(availablity.date, availablity.end_time)

    reserved_appointments = Appointment.objects.filter(
        staff = availablity.staff,
        date = availablity.date,
        status__in = [
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
            start_time = current_datetime.time()
        ).exists()

        if not is_reserved:
            slots.append({
                'start_time': current_datetime.time(),
                'end_time': slot_end_datetime.time()
            })
        current_datetime += timedelta(
            minutes=service_duration + gap
        )
        
    return slots