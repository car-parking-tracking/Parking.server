from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ParkingLotViewSet, FeaturesViewSet

router = DefaultRouter()
router.register(r'parking_lots', ParkingLotViewSet, basename='parkinglots')
router.register(
    r'feature_collection', FeaturesViewSet, basename='feature_collection'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
