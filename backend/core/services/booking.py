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

    # تبدیل تاریخ جلالی به میلادی
    gregorian_date = availability.date.togregorian()

    current_datetime = datetime.combine(
        gregorian_date,
        availability.start_time
    )

    end_datetime = datetime.combine(
        gregorian_date,
        availability.end_time
    )

    # گرفتن رزروهای ثبت‌شده
    reserved_appointments = Appointment.objects.filter(
        staff=availability.staff,
        date=gregorian_date,
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

        # اگر از ساعت کاری رد شد
        if slot_end_datetime > end_datetime:
            break

        # چک رزرو بودن
        is_reserved = reserved_appointments.filter(
            start_time=current_datetime.time()
        ).exists()

        slots.append({
            'date': str(availability.date),  # جلالی برای فرانت
            'start_time': current_datetime.time(),
            'end_time': slot_end_datetime.time(),
            'is_available': not is_reserved
        })

        current_datetime += timedelta(
            minutes=service_duration + gap
        )

    return slots