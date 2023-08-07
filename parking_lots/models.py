from django.core.validators import MinValueValidator
from django.db import models


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
    coordinates_x = models.FloatField(
        verbose_name='Координаты x',
        max_length=40,
        blank=False,
        unique=True,
    )
    coordinates_y = models.FloatField(
        verbose_name='Координаты y',
        max_length=40,
        blank=False,
        unique=True,
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
