from typing import List

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings as djoser_settings
from djoser.serializers import (TokenCreateSerializer, PasswordSerializer,
                                UserCreateSerializer, UserSerializer)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from parking_lots.models import ParkingLot

from users.models import CustomUser


class MyUserListSerializer(UserSerializer):
    """Сериализатор для работы с информацией о пользователях."""
    class Meta:
        model = CustomUser
        fields = ('email', 'id',
                  'first_name', 'last_name')


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name',
                  'last_name', 'password')


class UserPasswordSerializer(PasswordSerializer):
    """Сериализатор для проверки пароля на совпадение и неверного ввода."""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context.get('request').user
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError(
                {"new_password": "Пароли не должны совпадать"}
            )
        check_current = check_password(
            data['current_password'],
            user.password
        )
        if check_current is False:
            raise serializers.ValidationError(
                {"current_password": "Введен неверный пароль"}
            )
        return data


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


# class CustomTokenCreateSerializer(TokenCreateSerializer):
#     def validate(self, data):
#         password = data.get('password')
#         params = {
#             djoser_settings.LOGIN_FIELD: data.get(djoser_settings.LOGIN_FIELD)
#         }
#         self.user = authenticate(
#             request=self.context.get('request'),
#             **params,
#             password=password
#         )
#         if not self.user:
#             self.user = get_object_or_404(User, **params)
#             if self.user and not self.user.check_password(password):
#                 self.fail(_('Неверные данные'))
#
#         if not self.user:
#             self.fail(_('Неверные данные'))
#         return data


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
