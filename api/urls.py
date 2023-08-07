from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ParkingLotViewSet, FeaturesViewSet

router = SimpleRouter()
router.register('parking_lots', ParkingLotViewSet, basename='parkinglots')
router.register(
    'feature_collection', FeaturesViewSet, basename='feature_collection'
)

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
