from django.core.validators import MinValueValidator
from django.db import models

from .singleton import SingletonModel


class ParkingLot(models.Model):
    """
    Базовая модель для парковки, включает в себя координаты
    в формате x, y пример - 25.122923, 55.189352
    """
    address = models.CharField(
        verbose_name='Адрес парковки',
        max_length=150,
        blank=False,
    )
    latitude = models.FloatField(
        verbose_name='Широта',
        max_length=40,
        blank=False,
    )
    longitude = models.FloatField(
        verbose_name='Долгота',
        max_length=40,
        blank=False,
    )
    car_capacity = models.IntegerField(
        verbose_name='Общее количество парковочных мест',
        blank=False,
        unique=False,
        validators=[MinValueValidator(
            limit_value=1,
            message='Количество парковочных мест не может быть меньше одного'
        )]
    )
    tariffs = models.CharField(
        verbose_name='Стоимость парковки',
        max_length=2500,
        blank=False,
        unique=False
    )

    class Meta:
        verbose_name = 'Парковка'
        verbose_name_plural = 'Парковки'

    def __str__(self):
        return self.address


class CompanyInfo(SingletonModel):
    """
    Модель страницы 'О продукте'.
    """
    logo = models.ImageField(
        verbose_name='Лого',
        upload_to='parking_lots/logos/'
    )
    email = models.CharField(
        verbose_name='Адрес электронной почты',
        max_length=100
    )
    about = models.TextField(
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'О продукте'
        verbose_name_plural = 'О продукте'

    def __str__(self):
        return 'О продукте'
