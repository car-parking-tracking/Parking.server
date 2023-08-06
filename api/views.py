from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from parking_lots.models import ParkingLot
from .serializers import ParkingLotSerializer


class ParkingLotViewSet(viewsets.ModelViewSet):
    """
    List, retrieve and create parking lots.
    Accepts url parameters to filter objects: address:str, car_capacity:int.
    """

    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('address', 'car_capacity')
