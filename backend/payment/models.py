from uuid import uuid4

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from salon.models import Appointment


class Factor(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("successful", _("Successful")),
        ("failed", _("Failed")),
        ("refunded", _("Refunded")),
    )

    uuid = models.UUIDField(default=uuid4,unique=True,editable=False,verbose_name=_("uuid"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="factors", verbose_name=_("user"))
    payment_status = models.CharField(_("payment status"),max_length=20,choices=PAYMENT_STATUS_CHOICES,default="pending")
    total_price = models.PositiveIntegerField(_("total price"), default=0)
    transaction_datetime = models.DateTimeField(_("transaction datetime"),blank=True,null=True)

    datetime_created = models.DateTimeField(_("datetime created"),auto_now_add=True)
    datetime_modified = models.DateTimeField(_("datetime modified"), auto_now=True)

    def __str__(self):
        return f"Factor #{self.id}"


class PurchaseItem(models.Model):
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name="items", verbose_name=_("factor"))
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, blank=True, null=True, related_name="purchase_items", verbose_name=_("appointment"))
    title = models.CharField(_("title"), max_length=255)
    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    unit_price = models.PositiveIntegerField(_("unit price"))
    total_price = models.PositiveIntegerField(_("total price"))

    datetime_created = models.DateTimeField(_("datetime created"), auto_now_add=True)
    datetime_modified = models.DateTimeField(_("datetime modified"), auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("successful", _("Successful")),
        ("failed", _("Failed")),
    )

    factor = models.ForeignKey(Factor,on_delete=models.CASCADE,related_name="transactions",verbose_name=_("factor"))
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="transactions",verbose_name=_("user"))
    status = models.CharField(_("status"),max_length=20,choices=STATUS_CHOICES,default="pending")
    payment_authority = models.CharField(_("payment authority"),max_length=255,blank=True,null=True)
    ref_id = models.CharField(_("reference id"),max_length=255,blank=True,null=True)
    amount = models.PositiveIntegerField(_("amount"))
    code = models.IntegerField(_("gateway code"),blank=True,null=True)
    error_message = models.TextField(_("error message"),blank=True,null=True)
    gateway_response = models.JSONField(_("gateway response"),blank=True,null=True)
    payment_datetime = models.DateTimeField(_("payment datetime"),auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.id}"