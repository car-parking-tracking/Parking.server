from django.contrib import admin

from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Кастомизированная админка.
    Убрал поле is_superuser.
    """
    list_display = [
        'email',
        'is_staff',
        'is_active',
        'date_joined'
    ]
    list_filter = [
        'email',
        'is_staff',
        'is_active'
    ]
    readonly_fields = [
        'date_joined'
    ]
    fieldsets = [
        (
            None,
            {
                'fields': ['email', 'first_name', 'last_name', 'date_joined']
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
