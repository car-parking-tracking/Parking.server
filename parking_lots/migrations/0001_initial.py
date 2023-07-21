# Generated by Django 4.2.3 on 2023-07-21 11:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=150, verbose_name='Адрес парковки')),
                ('coordinates', models.CharField(max_length=40, unique=True, verbose_name='Координаты парковки')),
                ('car_capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Количество парковочных мест не может быть меньше одного')], verbose_name='Общее количество парковочных мест')),
                ('object_type', models.CharField(max_length=20, verbose_name='Тип парковки для отрисовки')),
            ],
            options={
                'verbose_name': 'Парковка',
                'verbose_name_plural': 'Парковки',
            },
        ),
    ]
