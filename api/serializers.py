from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings as djoser_settings
from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers

from parking_lots.models import ParkingLot

User = get_user_model()


class ParkingLotSerializer(serializers.ModelSerializer):
    is_favorited = serializers.BooleanField(read_only=True)

    class Meta:
        model = ParkingLot
        fields = [
            'id',
            'address',
            'coordinates_x',
            'coordinates_y',
            'car_capacity',
            'tariffs',
            'is_favorited'
        ]


class AddToFavsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = [
            'id'
        ]


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
            'coordinates': [obj.coordinates_x, obj.coordinates_y]
        }

    def get_properties(self, obj: ParkingLot) -> dict:
        return {
            'balloonContent': '<div id="parking"></div>',
        }


class FeatureCollectionSerializer(serializers.Serializer):
    type = serializers.CharField(default='FeatureCollection')
    features = serializers.SerializerMethodField()

    def get_features(self, obj):
        return FeatureSerializer(
            ParkingLot.objects.all(), many=True
        ).data
