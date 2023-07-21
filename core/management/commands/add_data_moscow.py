import json

from django.core.management import BaseCommand

from parking_lots.models import ParkingLot


class Command(BaseCommand):
    """
    Данный скрипт наполняет нашу базу данных данными из json файла
    московской парковки.
    Файл находится в /core/data/
    Запускается командой python manage.py add_data_moscow

    Пример json объекта:
    {
    "Address": "город Москва, улица Арбат, дом 54/2, строение 1",
    "CarCapacity": 5,
    "coordinates": [
      [
        [
          37.583203,
          55.746957
        ],
        [
          37.584011,
          55.747193
        ]
      ]
    ],
    "object_type": "MultiLineString"
    }
    """
    help = 'Наполнение базы данных информацией о платных московских парковках'

    def handle(self, *args, **options):
        json_file = 'core/data/moscow_parking.json'
        with open(json_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for parking_lot in json_data:
                ParkingLot.objects.create(
                    address=parking_lot['Address'],
                    coordinates=str(parking_lot['coordinates']),
                    car_capacity=parking_lot['CarCapacity'],
                    object_type=parking_lot['object_type']
                )
