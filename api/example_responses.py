from drf_yasg import openapi


LIST_FEATURES_EXAMPLE_RESPONSES = {
    "200": openapi.Response(
        description='ParkingLot wrapped as Feature example',
        examples={
            "application/json": {
                "type": "FeatureCollection",
                "features": [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [39.1, 48.5],
                        },
                        'properties': 'balloonContent: <div id=parking></div>'
                    },
                ]
            }
        }
    ),
}

LIST_PARKINGLOTS_EXAMPLE_RESPONSES = {
    "200": openapi.Response(
        description='ParkingLot example',
        examples={
            "application/json": {
                "count": 1,
                "next": "http://127.0.0.1/api/v1/parking_lots/?page=2",
                "previous": 'null',
                "results": [
                    {
                        'id': 1,
                        'is_favorited': True,
                        'address': 'Улица Пушкина, дом Колотушкина, 1',
                        'longitude': 35.7,
                        'latitude': 36.8,
                        'car_capacity': 43,
                        'tariffs': [
                            {
                                'TariffType': 'дифференцированный тариф',
                                'TimeRange': '00:00-23:59',
                                'FirstHalfHour': 20,
                                'FirstHour': 40,
                                'FollowingHours': 40
                            }
                        ]
                    }
                ]
            }
        }
    )
}
