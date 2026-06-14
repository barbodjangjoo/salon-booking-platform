from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class CustomUser(AbstractUser):
    username = None

    first_name = models.CharField(_('first_name'),max_length=255)
    last_name = models.CharField(_('last_name'),max_length=255)

    phone_number = models.CharField(_('phone_number'),max_length=12, unique=True)
    email = models.EmailField(_('email'),blank=True, null=True)

    datetime_created = models.DateTimeField(_('datetime_created'),auto_now_add=True)
    datetime_modified = models.DateTimeField(_('datetime_modified'),auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'
    
