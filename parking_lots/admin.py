from django.contrib import admin

from .models import ParkingLot


class ParkingLotAdmin(admin.ModelAdmin):
    """
    Черновая версия админки парковки.
    """
    list_display = [
        'address',
        'coordinates',
        'car_capacity'
    ]
    search_fields = ['address', ]


admin.site.register(ParkingLot, ParkingLotAdmin)
