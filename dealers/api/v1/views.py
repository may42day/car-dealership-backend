from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, permissions, status
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from cars.models import CarCharacteristic
from common.mixins import DealerOwnerMixin
from common.permissions import IsProfileOwnerOrReadOnly
from customers.filters import CustomerFilter
from customers.models import Customer
from dealers.api.v1.serializers import (
    DealerOwnerSerializer,
    DealerSerializer,
    DealerStockItemSerializer,
)
from dealers.filters import DealerFilter, DealerStockFilter
from dealers.models import Dealer, DealerStockItem
from dealers.permissions import IsDealerOwner, IsDealerOwnerOrReadOnly
from marketing.filters import (
    DealerDiscountFilter,
    DealerMarketingCampaignFilter,
)
from marketing.models import DealerDiscount, DealerMarketingCampaign
from orders.filters import DealerTotalDealsWithSupplierFilter
from orders.models import TotalSupplierPurchase
from suppliers.api.v1.serializers import SupplierSerializer
from suppliers.filters import SupplierFilter
from suppliers.models import Supplier
from marketing.api.v1.serializers import (
    DealerDiscountSerializer,
    DealerMarketingCampaignSerializer,
)
from orders.api.v1.serializers import (
    TotalDealerPurchaseSerializer,
    TotalSupplierPurchaseSerializer,
)
from users.models import UserProfile


class DealerAPIView(viewsets.ModelViewSet):
    """
    Dealer endpoint.

    This endpoint provides CRUD operations for dealers.
    Includes filtering and ordering dealer objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new dealer's entry.
    -POST : Add or remove car characteristics for dealer's profile.
    -GET : Retrieve a list of all dealers
    -GET : Retrieve a supplier's detail by dealer ID.
    -PUT/PATCH : Update dealer's data by ID.
    """

    queryset = Dealer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["foundation_date", "balance"]
    filterset_class = DealerFilter

    def get_serializer_class(self):
        """
        Function to get serializer class based on request user.
        """
        if self.request.user.is_staff or (
            "pk" in self.kwargs
            and self.request.user.role == UserProfile.DEALER
            and self.request.user.dealer.pk == int(self.kwargs.get("pk"))
        ):
            return DealerOwnerSerializer
        return DealerSerializer

    @action(methods=["POST"], detail=True, url_path="characteristics/add")
    def add_characteristics(self, request, pk):
        """
        Add car characteristics to dealer's profile.

        Returns:
        - 201 CREATED: If characteristic is added.
        - 400 Bad request: If there is no characteristic add in POST data.
        - 404 Not Found: If characteristic object does not exist.
        """
        dealer = self.get_object()
        car_characteristic_id = request.data.get("car_characteristic_id")

        if not car_characteristic_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        car_characteristic = get_object_or_404(
            CarCharacteristic, id=car_characteristic_id
        )
        dealer.car_characteristics.add(car_characteristic)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=True, url_path="characteristics/remove")
    def remove_characteristics(self, request, pk):
        """
        Remove car characteristics from dealer's profile.

        Returns:
        - 200 OK: If characteristic is removed.
        - 400 Bad request: If there is no characteristic add in POST data.
        - 404 Not Found: If characteristic object does not exist.
        """
        dealer = self.get_object()
        car_characteristic_id = request.data.get("car_characteristic_id")

        if not car_characteristic_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        car_characteristic = get_object_or_404(
            CarCharacteristic, id=car_characteristic_id
        )
        dealer.car_characteristics.remove(car_characteristic)
        return Response(status=status.HTTP_200_OK)


class DealerClientsDealsAPIView(generics.ListAPIView):
    """
    Dealers' clients' total purchases API endpoint.

    This endpoint provides a list of dealer's clients with their total purchases.
    Includes filtering dealer's clients objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all dealer's clinets total purchases.
    """

    serializer_class = TotalDealerPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsDealerOwner]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomerFilter

    def get_queryset(self):
        dealer_id = self.kwargs["pk"]
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.customers.all()
        except Dealer.DoesNotExist:
            return Customer.objects.none()


class DealerSuppliersDealsAPIView(generics.ListAPIView):
    """
    Dealers' suppliers' total purchases API endpoint.

    This endpoint provides a list of dealer's clients with their total purchases.
    Includes filtering dealer's supplier partners objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all dealer's clinets total purchases.
    """

    serializer_class = TotalSupplierPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsDealerOwner]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DealerTotalDealsWithSupplierFilter

    def get_queryset(self):

        dealer_id = self.kwargs["pk"]
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.orders_history.all()
        except Dealer.DoesNotExist:
            return TotalSupplierPurchase.objects.none()


class DealerSuppliersListAPIView(generics.ListAPIView):
    """
    Dealers' suppliers list API endpoint.

    This endpoint provides a list of dealer's partners with best offers.
    Includes filtering dealer's supplier partners objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all dealer's partners.
    """

    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsDealerOwner]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SupplierFilter

    def get_queryset(self):

        dealer_id = self.kwargs["pk"]
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.suppliers.all()
        except Dealer.DoesNotExist:
            return Supplier.objects.none()


class DealerStockAPIView(DealerOwnerMixin, viewsets.ModelViewSet):
    """
    Dealer stock endpoint.

    This endpoint provides CRUD operations for dealer's stock.
    Includes filtering and ordering dealer's stock item objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new dealer's stock item entry.
    -GET : Retrieve a list of all dealers' stock items.
    -GET : Retrieve a dealer's stock item detail by dealer ID.
    -PUT/PATCH : Update dealer's stock item data by ID.
    """

    queryset = DealerStockItem.objects.all()
    serializer_class = DealerStockItemSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsDealerOwnerOrReadOnly,
    ]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["price_per_one", "amount"]
    filterset_class = DealerStockFilter


class DealerDiscountListAPIView(generics.ListAPIView):
    """
    Dealers' discounts API endpoint.

    This endpoint provides a list of dealer's discounts.
    Includes filtering and ordering dealer's discounts objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all dealer's discounts.
    """

    serializer_class = DealerDiscountSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["min_amount", "percentage"]
    filterset_class = DealerDiscountFilter

    def get_queryset(self):
        dealer_id = self.kwargs["pk"]
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.discounts.all()
        except Dealer.DoesNotExist:
            return DealerDiscount.objects.none()


class DealerMarketingListAPIView(generics.ListAPIView):
    """
    Dealers' marketing campaigns API endpoint.

    This endpoint provides a list of dealer's marketing campaigns.
    Includes filtering and ordering dealer's marketing campaign objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all dealer's marketing campaigns.
    """

    serializer_class = DealerMarketingCampaignSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["min_amount", "percentage"]
    filterset_class = DealerMarketingCampaignFilter

    def get_queryset(self):
        dealer_id = self.kwargs["pk"]
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.marketing_campaigns.all()
        except Dealer.DoesNotExist:
            return DealerMarketingCampaign.objects.none()
