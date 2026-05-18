from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    is_phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'
    
