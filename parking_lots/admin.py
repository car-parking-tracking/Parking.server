import json

from django.contrib import admin

from .models import ParkingLot, CompanyInfo


class ParkingLotAdmin(admin.ModelAdmin):
    '''
    Админка парковки.
    Вместо списка тарифов отображается их количество.
    '''
    list_display = ('address', 'get_coordinates',
                    'car_capacity', 'get_tariffs_count')
    search_fields = ('address',)

    def get_coordinates(self, obj):
        return obj.latitude, obj.longitude
    get_coordinates.short_description = 'Координаты'

    def get_tariffs_count(self, obj):
        tariffs = json.loads(obj.tariffs.replace("'", "\""))
        return len(tariffs)
    get_tariffs_count.short_description = 'Количество тарифов'


admin.site.register(ParkingLot, ParkingLotAdmin)
admin.site.register(CompanyInfo)

admin.site.site_title = 'Администрирование Parkonaft'
admin.site.site_header = 'Администрирование Parkonaft'
