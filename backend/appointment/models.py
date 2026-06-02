from django.db import models
from django_jalali.db import models as jmodels

from core import models as coremodel


class Slot(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("blocked", "Blocked"),
    )
    staff = models.ForeignKey(coremodel.Staff, on_delete=models.CASCADE)
    availability = models.ForeignKey(
        coremodel.Availability, on_delete=models.CASCADE, related_name="slots"
    )
    date = jmodels.jDateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=9)

    def __str__(self):
        return f"{self.staff} Time: {self.start_time}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["staff", "date", "start_time"], name="unique_slot_per_staff"
            )
        ]


class Appointment(models.Model):
    BOOKING_CHOICES = (
        ("online", "Online"),
        ("walk_in", "Walk in"),
        ("phone", "Phone"),
    )

    customer = models.ForeignKey(
        coremodel.CustomUser, on_delete=models.CASCADE, related_name="appointments"
    )
    staff = models.ForeignKey(
        coremodel.Staff, on_delete=models.CASCADE, related_name="appointments"
    )
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT)
    service = models.ForeignKey(coremodel.Service, on_delete=models.CASCADE)
    booking_source = models.CharField(choices=BOOKING_CHOICES, max_length=7)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer} - {self.service}"
