from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager
from parking_lots.models import ParkingLot


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    username = None
    email = models.EmailField(
        verbose_name=_('адрес электронной почты'),
        unique=True
    )
    first_name = models.CharField(
        blank=True, max_length=150, verbose_name=_('имя')
    )
    last_name = models.CharField(
        blank=True, max_length=150, verbose_name=_('фамилия')
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('дата регистрации')
    )
    favorites = models.ManyToManyField(
        ParkingLot,
        related_name='favorites',
        verbose_name=_('избранное'),
    )

    USERNAME_FIELD = 'email'

    # для требуемых для заполнения полей в промптах
    # при создании суперпользователя через консоль
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
