from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
import string
import secrets
from django_jalali.db import models as jmodels

from salon.models import Service

class Factor(models.Model):
    PAYMENT_CHOICES =[
        ('pending', _('Pending')),
        ('successful', _('Successful')),
        ('failed', _('Failed'))
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="pending")
    datetime_transaction = jmodels.jDateField(blank=True, null=True)
    total_price = models.IntegerField()

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.payment_status}"

class PurchaseItem(models.Model):
    PAYMENT_CHOICES =[
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed')
    ]
    user= models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name='purchase_items')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL)
    price = models.IntegerField()
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='pending')

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.type}"
    