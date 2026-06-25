from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    resource_class = models.CustomUser
    list_display = [
        'id',
        'first_name',
        'last_name',
        'phone_number',
    ]
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number',
                'password1',
                'password2',
            ),
        }),
    )