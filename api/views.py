from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from djoser.views import UserViewSet
from djoser.serializers import ActivationSerializer
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from parking_lots.models import ParkingLot
from users.models import CustomUser
from .example_responses import (LIST_FEATURES_EXAMPLE_RESPONSES,
                                LIST_PARKINGLOTS_EXAMPLE_RESPONSES)

from .serializers import (ParkingLotSerializer, FeatureCollectionSerializer,
                          CustomUserSerializer, CustomUserCreateSerializer)


@method_decorator(
    decorator=swagger_auto_schema(
        responses=LIST_PARKINGLOTS_EXAMPLE_RESPONSES
    ),
    name='list'
)
class ParkingLotViewSet(viewsets.ModelViewSet):
    """
    List, retrieve and create parking lots.
    Accepts url parameters to filter objects: address:str, car_capacity:int.
    Supports searching by id, finds objects with ids that contain num passed
    in search url parameter.
    """
    serializer_class = ParkingLotSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']
    queryset = ParkingLot.objects.all()

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_fields = ('address', 'car_capacity')
    search_fields = ('^id',)
    ordering = ('id',)

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


@method_decorator(
    decorator=swagger_auto_schema(
        responses=LIST_FEATURES_EXAMPLE_RESPONSES
    ),
    name='list'
)
class FeaturesViewSet(ParkingLotViewSet):
    """
    List, retrieve parking lots with json needed
    for drawing points on map. Supports searching by id,
    finds objects with ids that contain num passed
    in search url parameter.
    """
    serializer_class = FeatureCollectionSerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_fields = ('address', 'car_capacity')
    search_fields = ('^id',)
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        serializer = FeatureCollectionSerializer(
            request.data, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Retrieving is disabled and will be later removed from urls."""
        return Response({'error': 'retrieving is not allowed'})


class CustomUserViewSet(UserViewSet):
    """
    List, retrieve, create, delete, activate users.
    me/ for showing current user (by passed auth token).
    """
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        if self.action == 'activation':  # Это костыль, надо переписать метод или убрать его в принципе
            return ActivationSerializer
        return CustomUserSerializer
