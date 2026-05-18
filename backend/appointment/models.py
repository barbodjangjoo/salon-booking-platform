from django.db import models

from core import models
class Appointment(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    customer = models.ForeignKey(models.CustomUser, on_delete=models.CASCADE, related_name='appointments')

    staff = models.ForeignKey(models.Staff, on_delete=models.CASCADE, related_name='appointments')

    service = models.ForeignKey(models.Service, on_delete=models.CASCADE)

    date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.customer} - {self.service}'