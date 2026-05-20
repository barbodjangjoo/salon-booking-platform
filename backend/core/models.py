from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    svg = models.FileField(upload_to='category_svg/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Services(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    requirement_time = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    svg = models.FileField(upload_to='service_svg/', blank=True, null=True)
    reserve_fee = models.IntegerField()

    def __str__(self):
        return self.title

class Staff(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ManyToManyField(Services)
    min_gap_between_appointments = models.PositiveIntegerField(
        default=0,
        help_text='Gap between appointments in minutes'
    )
    

class Availability(models.Model):
    staff = models.ForeignKey( Staff, on_delete=models.CASCADE, related_name='availabilities')

    date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.staff} - {self.date}'
