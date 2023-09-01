import json


def process():
    """
    Скрипт для процессинга сырого json от сайта парковок
    и приведения его к подобающему виду.
    """
    TIMESTAMPS = [
        '08:00-21:00',
        '21:00-23:59',
        '00:00-08:00',
    ]

    with open('raw_data.json', 'r', encoding='windows-1251') as file:
        json_context = file.read()

        data = json.loads(json_context)

        for obj in data:
            del obj['is_deleted']
            del obj['ID']
            del obj['ParkingName']
            del obj['ParkingZoneNumber']
            del obj['global_id']
            del obj['AdmArea']
            del obj['District']
            del obj['CarCapacityDisabled']
            del obj['Longitude_WGS84']
            del obj['Latitude_WGS84']
            obj['coordinates'] = obj['geodata_center']['coordinates']
            obj['tariffs'] = []

            unique_time_ranges = set()
            filtered_tariffs = []

            for tariff in obj["Tariffs"]:
                if tariff["TimeRange"] not in unique_time_ranges:
                    unique_time_ranges.add(tariff["TimeRange"])
                    filtered_tariffs.append(tariff)

            obj["tariffs"] = filtered_tariffs
            del obj['geoData']
            del obj['Coordinates']
            del obj['geodata_center']
            del obj['Tariffs']

    with open('moscow_parking.json', 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=2, ensure_ascii=False)
        print('Процессинг завершен')
