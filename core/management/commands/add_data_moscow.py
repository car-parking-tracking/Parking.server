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
      37.591079,
      55.778752
    ],
    }
    "tariffs" : []
    """
    help = 'Наполнение базы данных информацией о платных московских парковках'

    def handle(self, *args, **options):
        json_file = 'core/data/moscow_parking.json'
        with open(json_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for parking_lot in json_data:
                ParkingLot.objects.create(
                    address=parking_lot['Address'],
                    latitude=float(parking_lot['coordinates'][1]),
                    longitude=float(parking_lot['coordinates'][0]),
                    car_capacity=parking_lot['CarCapacity'],
                    tariffs=parking_lot['Tariffs']
                )
