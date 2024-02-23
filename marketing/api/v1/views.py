from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from common.mixins import DealerOwnerMixin, SupplierOwnerMixin
from marketing.api.v1.serializers import (
    DealerDiscountSerializer,
    DealerMarketingCampaignSerializer,
    SupplierDiscountSerializer,
    SupplierMarketingCampaignSerializer,
    DealerDiscount,
    SupplierDiscount,
)
from marketing.filters import (
    DealerDiscountFilter,
    DealerMarketingCampaignFilter,
    SupplierDiscountFilter,
    SupplierMarketingCampaignFilter,
)
from marketing.models import DealerMarketingCampaign, SupplierMarketingCampaign
from marketing.permissions import (
    IsMarketingDealerOwnerOrReadOnly,
    IsMarketingSupplierOwnerOrReadOnly,
)
from cars.models import Car


class UpdateCampaignCarsMixin:
    """
    Mixin for marketing campaigns APIs to add and remove cars.

    Methods:
    - cars/add: to add car to marketing campaign.
    - cars/remove: to remove car from marketing campaign.
    """

    @action(methods=["POST"], detail=True, url_path="cars/add")
    def add_cars(self, request, pk):
        """
        Add cars to dealer's marketing_campaign.

        Returns:
        - 201 CREATED: If car is added.
        - 400 Bad request: If there is no cars add in POST data.
        - 404 Not Found: If car object does not exist.
        """
        campaign = self.get_object()
        car_id = request.data.get("car_id")

        if not car_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        car = get_object_or_404(Car, id=car_id)
        campaign.cars.add(car)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=True, url_path="cars/remove")
    def remove_cars(self, request, pk):
        """
        Remove car characteristics from dealer's profile.

        Returns:
        - 200 OK: If car is removed.
        - 400 Bad request: If there is no cars add in POST data.
        - 404 Not Found: If car object does not exist.
        """
        campaign = self.get_object()
        car_id = request.data.get("car_id")

        if not car_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        car = get_object_or_404(Car, id=car_id)
        campaign.cars.remove(car)
        return Response(status=status.HTTP_200_OK)


class DealerMarketingCampaignAPIView(
    DealerOwnerMixin, UpdateCampaignCarsMixin, viewsets.ModelViewSet
):
    """
    Dealer marketing campaign endpoint.

    This endpoint provides CRUD operations for customers.
    Includes searching, filtering and ordering dealer's marketing campaigns objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new dealer's marketing campaign entry.
    -GET : Retrieve a list of all dealers' marketing campaigns.
    -GET : Retrieve a dealer's marketing campaigns detail by deaker ID.
    -PUT/PATCH : Update dealer's marketing campaign data by ID.
    """

    queryset = DealerMarketingCampaign.objects.all()
    serializer_class = DealerMarketingCampaignSerializer
    permission_classes = [permissions.IsAuthenticated, IsMarketingDealerOwnerOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["description", "name"]
    ordering_fields = ["end_date", "start_date", "percentage"]
    filterset_class = DealerMarketingCampaignFilter


class SuplierMarketingCampaignAPIView(
    SupplierOwnerMixin, UpdateCampaignCarsMixin, viewsets.ModelViewSet
):
    """
    Supplier marketing campaign endpoint.

    This endpoint provides CRUD operations for customers.
    Includes searching, filtering and ordering suppliers's marketing campaigns objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new supplier's marketing campaign entry.
    -GET : Retrieve a list of all suppliers' marketing campaigns.
    -GET : Retrieve a supplier's marketing campaigns detail by deaker ID.
    -PUT/PATCH : Update supplier's marketing campaign data by ID.
    """

    queryset = SupplierMarketingCampaign.objects.all()
    serializer_class = SupplierMarketingCampaignSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsMarketingSupplierOwnerOrReadOnly,
    ]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["description", "name"]
    ordering_fields = ["end_date", "start_date", "percentage"]
    filterset_class = SupplierMarketingCampaignFilter


class DealerDiscountsAPIView(DealerOwnerMixin, viewsets.ModelViewSet):
    """
    Dealer discount endpoint.

    This endpoint provides CRUD operations for customers.
    Includes filtering and ordering dealer's discounts objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new dealer's discount entry.
    -GET : Retrieve a list of all dealers' discounts.
    -GET : Retrieve a dealer's discounts detail by deaker ID.
    -PUT/PATCH : Update dealer's discount data by ID.
    """

    queryset = DealerDiscount.objects.all()
    serializer_class = DealerDiscountSerializer
    permission_classes = [permissions.IsAuthenticated, IsMarketingDealerOwnerOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["percentage", "min_amount"]
    filterset_class = DealerDiscountFilter


class SuplierDiscountsAPIView(SupplierOwnerMixin, viewsets.ModelViewSet):
    """
    Supplier discount endpoint.

    This endpoint provides CRUD operations for customers.
    Includes filtering and ordering dealer's discounts objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new supplier's discount entry.
    -GET : Retrieve a list of all suppliers' discounts.
    -GET : Retrieve a supplier's discounts detail by deaker ID.
    -PUT/PATCH : Update supplier's discount data by ID.
    """

    queryset = SupplierDiscount.objects.all()
    serializer_class = SupplierDiscountSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsMarketingSupplierOwnerOrReadOnly,
    ]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["percentage", "min_amount"]
    filterset_class = SupplierDiscountFilter
