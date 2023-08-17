# Generated by Django 4.2.3 on 2023-08-15 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lots', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favorites',
            field=models.ManyToManyField(related_name='favorites', to='parking_lots.parkinglot', verbose_name='избранное'),
        ),
    ]
