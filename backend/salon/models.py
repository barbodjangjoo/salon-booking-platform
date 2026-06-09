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
        Category,
        on_delete=models.PROTECT,
        related_name="services",
        verbose_name=_("category"),
    )
    title = models.CharField(_("title"), max_length=255)
    duration = models.PositiveIntegerField(
        _("duration"), help_text=_("Duration in minutes")
    )
    reserve_fee = models.IntegerField(_("reserve_fee"))

    def __str__(self):
        return self.title


class Staff(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("user"),
    )
    service = models.ManyToManyField(
        Service, related_name="staff", verbose_name=_("service")
    )
    min_gap_between_appointments = models.PositiveIntegerField(
        _("gap between appointments"),
        default=0,
        help_text=_("Gap between appointments in minutes"),
    )

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name}"


class Availability(models.Model):
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="availabilities",
        verbose_name=_("staff"),
    )

    date = jmodels.jDateField(_("date"))

    start_time = models.TimeField(_("start time"))
    end_time = models.TimeField(_("end time"))

    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return f"{self.staff} - {self.date}"


class Slot(models.Model):
    STATUS_CHOICES = (
        ("available", _("Available")),
        ("reserved", _("Reserved")),
        ("blocked", _("Blocked")),
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name=_("staff"))
    availability = models.ForeignKey(
        Availability,
        on_delete=models.CASCADE,
        related_name="slots",
        verbose_name=_("availability"),
    )
    date = jmodels.jDateField(_("date"))
    start_time = models.TimeField(_("start time"))
    end_time = models.TimeField(_("end time"))
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=9, verbose_name=_("status")
    )

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
        ("online", _("Online")),
        ("walk_in", _("Walk in")),
        ("phone", _("Phone")),
    )

    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("customer"),
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name=_("staff"),
    )
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT, verbose_name=_("slot"))
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name=_("service")
    )
    booking_source = models.CharField(
        choices=BOOKING_CHOICES, max_length=7, verbose_name=_("booking source")
    )

    datetime_created = models.DateTimeField(_("datetime created"), auto_now_add=True)
    datetime_modified = models.DateTimeField(_("datetime modified"), auto_now=True)

    def __str__(self):
        return f"{self.customer} - {self.service}"
