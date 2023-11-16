from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings as djoser_settings
from djoser.serializers import TokenCreateSerializer, UserCreateSerializer
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_yasg.utils import swagger_serializer_method

from parking_lots.models import ParkingLot, CompanyInfo

User = get_user_model()


class ParkingLotSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = ParkingLot
        fields = (
            'id',
            'is_favorited',
            'address',
            'longitude',
            'latitude',
            'car_capacity',
            'tariffs',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return request.user.favorites.filter(id=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей"""
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        )


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    favorites = ParkingLotSerializer(many=True, read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'favorites',
        )


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, data):
        password = data.get('password')
        params = {
            djoser_settings.LOGIN_FIELD: data.get(djoser_settings.LOGIN_FIELD)
        }
        self.user = authenticate(
            request=self.context.get('request'),
            **params,
            password=password
        )
        if not self.user:
            self.user = get_object_or_404(User, **params)
            if self.user and not self.user.check_password(password):
                self.fail(_('Неверные данные'))

        if not self.user:
            self.fail(_('Неверные данные'))
        return data


class FeatureSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='Feature')
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = ParkingLot
        fields = [
            'type',
            'id',
            'geometry',
            'properties',
        ]

    def get_geometry(self, obj: ParkingLot) -> dict:
        return {
            'type': 'Point',
            'coordinates': [obj.latitude, obj.longitude]
        }

    def get_properties(self, obj: ParkingLot) -> dict:
        return {
            'balloonContent': '<div id="parking"></div>',
        }


class FeatureCollectionSerializer(serializers.Serializer):
    type = serializers.CharField(default='FeatureCollection')
    features = serializers.SerializerMethodField()

    @swagger_serializer_method(
        serializer_or_field=FeatureSerializer(many=True)
    )
    def get_features(self, obj):
        id = self.context['request'].query_params.get('search')
        if id:
            return FeatureSerializer(
                ParkingLot.objects.filter(id__startswith=id).all(), many=True
            ).data
        return FeatureSerializer(
            ParkingLot.objects.all(), many=True
        ).data


class CompanyInfoSerializer(serializers.ModelSerializer):

    logo = Base64ImageField()
    image = Base64ImageField()

    class Meta:
        model = CompanyInfo
        fields = (
            'logo',
            'image',
            'email',
            'about',
            )
