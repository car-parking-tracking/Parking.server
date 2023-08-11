from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import FeaturesViewSet, MyUserViewSet, ParkingLotViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r'users', MyUserViewSet, basename='users')
router.register('parking_lots', ParkingLotViewSet, basename='parkinglots')
router.register(
    'feature_collection', FeaturesViewSet, basename='feature_collection'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
