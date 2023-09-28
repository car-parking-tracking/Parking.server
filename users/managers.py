from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Переопределение уникального поля для авторизации.
    Для последующего дополнения модели User кастомными полями.
    Отделение создания суперпользователя от обычного пользователя.
    """

    def create_user(self, email, password, **fields):
        """
        Создание пользователя по почте и паролю.
        """
        if not email:
            raise ValueError(_('Необходимо указать почту'))

        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **fields):
        """
        Создание суперпользователя с необходимыми атрибутами
        по умолчанию.
        """
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)
        fields.setdefault('is_active', True)

        if fields.get('is_staff') is False:
            raise ValueError(
                _('Суперпользователь должен иметь атрибут is_staff=True')
            )
        if fields.get('is_superuser') is False:
            raise ValueError(
                _('Суперпользователь должен иметь атрибут is_superuser=True')
            )
        return self.create_user(email, password, **fields)
