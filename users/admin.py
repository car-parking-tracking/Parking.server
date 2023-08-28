from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Кастомизированная админка.
    Убрал поле is_superuser.
    """
    list_display = [
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'favorites'
    ]
    list_filter = [
        'email',
        'is_staff',
        'is_active'
    ]
    readonly_fields = [
        'date_joined',
    ]
    fieldsets = [
        (
            None,
            {
                'fields': ['email', 'first_name', 'last_name', 'date_joined', 'favorites']
            }
        ),
        (
            'Permissions',
            {
                'fields': [
                    'is_staff', 'is_active', 'groups', 'user_permissions'
                ]
            }
        )
    ]

    def favorites(self, obj):
        return obj.favorites.all()
