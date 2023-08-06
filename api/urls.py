from django.urls import path, include
from rest_framework.routers import SimpleRouter


from .views import ParkingLotViewSet


router = SimpleRouter()
router.register('parking_lots', ParkingLotViewSet, basename='parkinglots')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
