from django.contrib.auth.hashers import check_password
from djoser.serializers import (PasswordSerializer,
                                UserCreateSerializer, UserSerializer)
from rest_framework import serializers

from parking_lots.models import ParkingLot
from users.models import CustomUser


class MyUserListSerializer(UserSerializer):
    """Вывод информации о зарегистрированном пользователе."""
    class Meta:
        model = CustomUser
        fields = ('email', 'id',
                  'first_name', 'last_name')


class MyUserCreateSerializer(UserCreateSerializer):
    """Ввод информации для регистрации пользователя."""
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name',
                  'last_name', 'password')


class UserPasswordSerializer(PasswordSerializer):
    """Проверка пароля на совпадение и неверного ввода."""
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
            'latitude',
            'longitude',
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

    def get_features(self, obj):
        return FeatureSerializer(
            ParkingLot.objects.all(), many=True
        ).data
