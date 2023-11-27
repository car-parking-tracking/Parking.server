import json

from django.core.management import BaseCommand

from parking_lots.models import ParkingLot


class Command(BaseCommand):
    """
    Данный скрипт наполняет нашу базу данных данными из json файла
    московской парковки.
    Файл находится в /parser/
    Запускается командой python manage.py add_data_moscow

    Пример json объекта:
    {
    "Address": "город Москва, улица Арбат, дом 54/2, строение 1",
    "CarCapacity": 5,
        "coordinates": [
      37.591079,
      55.778752
    ],
    }
    "tariffs" : []
    """
    help = 'Наполнение базы данных информацией о платных московских парковках'

    def handle(self, *args, **options):
        json_file = 'parser/moscow_parking.json'
        with open(json_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for parking_lot in json_data:
                address = parking_lot['Address']
                defaults = {
                    'latitude': float(parking_lot['coordinates'][1]),
                    'longitude': float(parking_lot['coordinates'][0]),
                    'car_capacity': parking_lot['CarCapacity'],
                    'tariffs': parking_lot['tariffs']
                }

                existing_parking_lot, created = ParkingLot.objects.get_or_create(
                    address=address,
                    defaults=defaults
                )

                if not created:
                    for field, value in defaults.items():
                        setattr(existing_parking_lot, field, value)
                    existing_parking_lot.save()
        print('Данные обновлены')
