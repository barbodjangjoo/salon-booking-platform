from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class Category(models.Model):
    title = models.CharField(_("title"), max_length=255)

    def __str__(self):
        return self.title


class Service(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="services"
    )
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    reserve_fee = models.IntegerField()

    def __str__(self):
        return self.title


class Staff(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    service = models.ManyToManyField(Service, related_name="staff")
    min_gap_between_appointments = models.PositiveIntegerField(
        default=0, help_text="Gap between appointments in minutes"
    )

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name}"


class Availability(models.Model):
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="availabilities"
    )

    date = jmodels.jDateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.staff} - {self.date}"


class Slot(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("blocked", "Blocked"),
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    availability = models.ForeignKey(
        Availability, on_delete=models.CASCADE, related_name="slots"
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
        get_user_model(), on_delete=models.CASCADE, related_name="appointments"
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="appointments"
    )
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_source = models.CharField(choices=BOOKING_CHOICES, max_length=7)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer} - {self.service}"
