from django.apps import AppConfig


class UsersConfig(AppConfig):
    verbose_name = 'Пользователи'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from . import signals  # noqa
