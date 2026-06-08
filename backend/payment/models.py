from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
import string
import secrets
from django_jalali.db import models as jmodels

def generate_voucher_code():
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))
class VoucherCode(models.Model):
    VOUCHER_CHOICES = [
        ('PERCENT', 'Percent'),
        ('INTEGER', 'Integer')
    ]
    title = models.CharField(max_length=255)
    voucher_type = models.CharField(choices=VOUCHER_CHOICES, max_length=7)
    amount = models.IntegerField()
    code = models.CharField(max_length=8, default=generate_voucher_code)
    is_active = models.BooleanField(default=True)
    max_usage = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    expires_at = jmodels.jDateField(_('expire_at'))

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

class Factor(models.Model):
    PAYMENT_CHOICES =[
        ('pending', _('Pending')),
        ('successful', _('Successful')),
        ('failed', _('Failed'))
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="pending")
    datetime_transaction = models.DateTimeField(blank=True, null=True)
    total_price = models.IntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.payment_status}"
