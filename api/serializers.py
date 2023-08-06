from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from djoser.conf import settings as djoser_settings
from djoser.serializers import TokenCreateSerializer

from parking_lots.models import ParkingLot


User = get_user_model()


class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = [
            'id',
            'address',
            'coordinates',
            'car_capacity',
            'object_type',
            'tariffs',
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

        if self.user:
            return data
        self.fail(_('Неверные данные'))
