from django.contrib import admin

from . import models

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    resource_class = models.CustomUser
    list_display = [
        'id',
        'first_name',
        'last_name',
        'phone_number',
        'is_phone_verified'
    ]
