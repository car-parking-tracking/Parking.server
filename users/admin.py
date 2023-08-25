from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Кастомизированная админка.
    Позволяет создать нового пользователя.
    """
    list_display = (
        'email',
        'is_staff',
        'is_active',
        'date_joined',
    )
    list_filter = (
        'email',
        'is_staff',
        'is_active'
    )
    ordering = ('email',)
    readonly_fields = (
        'date_joined',
    )
    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'first_name', 'last_name', 'date_joined')
            }
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff', 'is_active', 'groups', 'user_permissions'
                )
            }
        )
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'is_staff'
                ),
            },
        ),
    )

    def favorites(self, obj):
        return obj.favorites.all()
