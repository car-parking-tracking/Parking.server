# from rest_framework.permissions import IsAuthenticated
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
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

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

    @staticmethod
    def create_delete(
        query, request, parking_lot: ParkingLot, error_messages: dict, pk=None
    ):
        """Для наследования эндпоинтами типа добавить в manytomany."""
        parking_lot = get_object_or_404(ParkingLot, id=pk)

        if request.method == 'POST':
            if query.filter(id=parking_lot.id).exists():
                return Response(
                    data={
                        'errors': error_messages['exists']
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            query.add(parking_lot)
            serializer = ParkingLotSerializer(parking_lot)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        if not query.filter(id=parking_lot.id).exists():
            return Response(
                data={
                    'errors': error_messages['!exists']
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        query.remove(parking_lot)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        serializer_class=AddToFavsSerializer
    )
    def favorite(self, request, pk=None):
        """Adding parking lot to favorites."""
        recipe = get_object_or_404(ParkingLot, id=pk)
        user = request.user

        return self.create_delete(
            user.favorites, request=request, recipe=recipe,
            error_messages={
                'exists': 'Парковка уже добавлена в избранное.',
                '!exists': 'Парковки нет в избранном.'
            },
            pk=pk
        )


class FeaturesViewSet(ParkingLotViewSet):
    """List, retrieve parking lots with json needed
    for drawing points on map."""
    serializer_class = FeatureCollectionSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """Переопределил метод, чтобы сериализатор не применялся
        несколько раз (к каждому объекту querysey), а только единожды
        ко всему queryset."""
        serializer = FeatureCollectionSerializer(request.data)
        return Response(serializer.data)
