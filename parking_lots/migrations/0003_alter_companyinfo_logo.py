# Generated by Django 4.2.3 on 2023-09-12 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lots', '0002_companyinfo_alter_parkinglot_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='logo',
            field=models.ImageField(upload_to='company_info/logos/', verbose_name='Лого'),
        ),
    ]
