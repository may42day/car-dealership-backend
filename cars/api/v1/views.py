from rest_framework import mixins, viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from cars.api.v1.serializers import CarSerializer, CarCharacteristicSerializer
from cars.services import pick_up_car_by_characteristic
from cars.models import Car, CarCharacteristic
from common.permissions import IsCompanyOrReadOnly
from cars.filters import CarCharacteristicFilter, CarFilter


class CarFiltersMixin:
    """
    A mixin class with filter backends and fields for searching, ordering for views related to cars.

    Attributes
    ----------
    - filter_backends : tuple of filter classes.
    - search_fields : fields for searching car objects.
    - ordering_fields : fields for ordering car objects.
    """

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["brand", "car_model", "generation"]
    ordering_fields = ["year_release", "year_end_of_production"]


class CarAPIView(
    CarFiltersMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Car API endpoint.

    Includes mixin for filtering, searching and ordering car objects.

    HTTP methods:
    - GET
    - POST

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new car
    -GET : Retrieve a list of all cars
    -GET : Retrieve A car's detail by ID
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyOrReadOnly]
    filterset_class = CarFilter


class CarCharacteristicAPIView(
    CarFiltersMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Car CarCharacteristic API endpoint.

    Includes mixin for filtering, searching and ordering car characteristic objects.

    HTTP methods:
    - GET
    - POST

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new car characteristic.
    -GET : Retrieve a list of all car characteristic
    -GET : Retrieve a car characteristic's detail by ID
    """

    queryset = CarCharacteristic.objects.all()
    serializer_class = CarCharacteristicSerializer
    filterset_class = CarCharacteristicFilter

    @action(methods=["get"], detail=True, url_path="pick-up-cars")
    def pick_up_cars(self, request, pk=None):
        characteristic = self.get_object()
        cars = Car.objects.all()
        if cars:
            filtered_cars = pick_up_car_by_characteristic(
                characteristic, cars, exact_match=True
            )
            serializer = CarSerializer(filtered_cars, many=True)
            return Response(data=serializer.data)

        return Response({"cars": None})
