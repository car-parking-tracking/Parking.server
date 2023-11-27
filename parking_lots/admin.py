import json

from django.contrib import admin

from .models import ParkingLot, CompanyInfo


@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    '''
    Админка парковки.
    Вместо списка тарифов отображается их количество.
    '''
    list_display = ('address', 'get_coordinates',
                    'car_capacity', 'get_tariffs_count')
    search_fields = ('address',)
    list_per_page = 10

    @admin.display(description='Координаты')
    def get_coordinates(self, obj):
        return obj.latitude, obj.longitude

    @admin.display(description='Количество тарифов')
    def get_tariffs_count(self, obj):
        tariffs = json.loads(obj.tariffs.replace("'", "\""))
        return len(tariffs)


admin.site.register(CompanyInfo)

admin.site.site_title = 'Администрирование Parkonaft'
admin.site.site_header = 'Администрирование Parkonaft'
