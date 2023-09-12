from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ParkingLotViewSet, FeaturesViewSet,
                    CustomUserViewSet, CompanyInfoView)

router = DefaultRouter()
router.register(r'parking_lots', ParkingLotViewSet, basename='parkinglots')
router.register(
    r'feature_collection', FeaturesViewSet, basename='feature_collection'
)
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),  # От дублирования лучше избавиться
    path('company_info/', CompanyInfoView.as_view()),
]
