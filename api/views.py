from rest_framework.permissions import AllowAny
from django.db.models import Case, When, BooleanField
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from parking_lots.models import ParkingLot

from .serializers import ParkingLotSerializer, FeatureCollectionSerializer, \
    AddToFavsSerializer


class ParkingLotViewSet(viewsets.ModelViewSet):
    """
    List, retrieve and create parking lots.
    Accepts url parameters to filter objects: address:str, car_capacity:int.
    """
    serializer_class = ParkingLotSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('address', 'car_capacity')

    def get_queryset(self):
        """Аннотация queryset для фильтрации парковок по вхождению
        в избранное пользователя."""
        favorites = []
        if not self.request.user.is_anonymous:
            favorites = self.request.user.favorites.values('id')

        return ParkingLot.objects.all().annotate(
            is_favorited=Case(
                When(id__in=favorites, then=True),
                default=False,
                output_field=BooleanField()
            )
        )

    @action(
        detail=True,
        methods=['post'],
        serializer_class=AddToFavsSerializer,
        http_method_names=['post']
    )
    def favorite(self, request, pk=None):
        """Adding parking lot to favorites."""
        parking_lot = get_object_or_404(ParkingLot, id=pk)
        user = request.user

        if user.favorites.filter(id=parking_lot.id).exists():
            user.favorites.remove(parking_lot)
        else:
            user.favorites.add(parking_lot)

        serializer = ParkingLotSerializer(parking_lot)
        serializer.context['request'] = self.request
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class FeaturesViewSet(ParkingLotViewSet):
    """List, retrieve parking lots with json needed
    for drawing points on map."""
    serializer_class = FeatureCollectionSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """Переопределил метод, чтобы сериализатор не применялся
        несколько раз (к каждому объекту queryset), а только единожды
        ко всему queryset."""
        serializer = FeatureCollectionSerializer(request.data)
        return Response(serializer.data)
