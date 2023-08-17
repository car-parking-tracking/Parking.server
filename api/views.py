from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from parking_lots.models import ParkingLot

from .serializers import ParkingLotSerializer, FeatureCollectionSerializer


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

    @action(
        detail=True,
        methods=['post'],
        serializer_class=ParkingLotSerializer,
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

        serializer = self.get_serializer(parking_lot)
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
