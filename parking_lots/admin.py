from django.contrib import admin

from .models import ParkingLot


class ParkingLotAdmin(admin.ModelAdmin):
    """
    Черновая версия админки парковки.
    """
    list_display = [
        'address',
        'get_coordinates',
        'car_capacity'
    ]
    search_fields = ['address', 'car_capacity']

    def get_coordinates(self, obj):
        return obj.coordinates_x, obj.coordinates_y


admin.site.register(ParkingLot, ParkingLotAdmin)
