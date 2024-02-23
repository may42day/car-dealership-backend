from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from common.mixins import CustomerOwnerMixin, DealerOwnerMixin
from customers.models import Customer
from customers.permissions import IsActiveUserOrReadOnly, IsCustomerOrReadOnly
from dealers.models import Dealer
from dealers.permissions import IsDealerOrReadOnly, IsDealerOwner
from orders.api.v1.serializers import (
    CustomerDealsHistorySerializer,
    CustomerOfferSerializer,
    DealerDealsHistorySerializer,
    DealerOfferSerializer,
    TotalDealerPurchaseSerializer,
    TotalSupplierPurchaseSerializer,
)
from orders.filters import (
    CustomerDealsHistoryFilter,
    DealerDealsWithCustomerFilter,
    DealerDealsWithSupplierFilter,
    DealerTotalDealsWithCustomerFilter,
    DealerTotalDealsWithSupplierFilter,
    SupplierDealsWithDealerFilter,
    SupplierTotalDealsWithDealerFilter,
)
from orders.models import (
    CustomerDealsHistory,
    CustomerOffer,
    DealerDealsHistory,
    DealerOffer,
    TotalDealerPurchase,
    TotalSupplierPurchase,
)
from orders.tasks import handle_customer_offer, handle_dealer_offer
from suppliers.models import Supplier
from suppliers.permissions import IsSupplierOwner


class CustomersDealsHistoryView(generics.ListAPIView, generics.RetrieveAPIView):
    """
    Customer's deals history API endpoint.

    This endpoint provides a list of all customers' orders or orders of specific customer.
    Includes filtering and ordering customer deals objects.

    HTTP methods:
    - GET


    Request parameters:
    - id (path parameter, optional)

    Actions:
    -GET : Retrieve a list of all customer's cars
    -GET : Retrieve orders of specific customer
    """

    serializer_class = CustomerDealsHistorySerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["price_per_one", "amount", "date"]
    filterset_class = CustomerDealsHistoryFilter

    def get_queryset(self):
        customer_id = self.kwargs.get("pk")
        if customer_id:
            try:
                customer = Customer.objects.get(pk=customer_id)
                return customer.history.all()
            except Customer.DoesNotExist:
                return CustomerDealsHistory.objects.none()
        return CustomerDealsHistory.objects.all()


class CustomersOffersAPIView(CustomerOwnerMixin, generics.ListCreateAPIView):
    """
    Customer's offers API endpoint.

    This endpoint provides a list of offers of specific customer.
    Includes filtering and ordering customer offers objects.

    HTTP methods:
    - GET
    - POST

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of customer's offers
    -POST : Create customer offer and task for handling it.
    """

    serializer_class = CustomerOfferSerializer
    queryset = CustomerOffer.objects.all().select_related(
        "customer", "car", "characteristic"
    )
    permission_classes = [
        permissions.IsAuthenticated,
        IsCustomerOrReadOnly,
        IsActiveUserOrReadOnly,
    ]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["max_price", "amount"]
    filterset_fields = ["car", "is_closed"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        offer = serializer.save()

        handle_customer_offer.delay(offer.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomersOffersRetrieveAPIView(generics.RetrieveAPIView):
    """
    Customer's offers API endpoint.

    This endpoint to retrieve specific offer.
    Includes filtering and ordering customer offers objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a specific offer.
    """

    serializer_class = CustomerOfferSerializer
    queryset = CustomerOffer.objects.all().select_related(
        "customer", "car", "characteristic"
    )
    permission_classes = [
        permissions.IsAuthenticated,
        IsCustomerOrReadOnly,
        IsActiveUserOrReadOnly,
    ]


class DealersOffersAPIView(DealerOwnerMixin, generics.ListCreateAPIView):
    """
    Dealer's retrieve offers API endpoint.

    This endpoint provides a list of offers of specific dealer.
    Includes filtering and ordering dealer offers objects.

    HTTP methods:
    - GET
    - POST

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of dealer's offers
    -POST : Create dealer offer and task for handling it.
    """

    serializer_class = DealerOfferSerializer
    queryset = DealerOffer.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsDealerOrReadOnly,
        IsActiveUserOrReadOnly,
    ]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["max_price", "amount"]
    filterset_fields = ["car", "is_closed"]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        offer = serializer.save()

        handle_dealer_offer.delay(offer.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DealersOffersRetrieveAPIView(generics.RetrieveAPIView):
    """
    Dealer's retrieve offers API endpoint.

    This endpoint to retrieve specific dealer's offer.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a specific offer.
    """

    serializer_class = DealerOfferSerializer
    queryset = DealerOffer.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsDealerOrReadOnly,
        IsActiveUserOrReadOnly,
    ]


class DealersHistoryWithCustomersView(generics.ListAPIView):
    """
    Dealer's deals with customers API endpoint.

    This endpoint provides a list of deals with customers of specific dealer.
    Includes filtering and ordering customer deals objects.

    HTTP methods:
    - GET


    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of customers' deals with specific dealer.
    """

    serializer_class = CustomerDealsHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsDealerOwner]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["amount", "price_per_one", "date"]
    filterset_class = DealerDealsWithCustomerFilter

    def get_queryset(self):
        dealer_id = self.kwargs.get("pk")
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.customer_history.all()
        except Dealer.DoesNotExist:
            return CustomerDealsHistory.objects.none()


class DealersTotalHistoryWithCustomersView(generics.ListAPIView):
    """
    Dealer's total deals with customers API endpoint.

    This endpoint provides a list of total deals of dealer's customer.
    Includes filtering and ordering dealer's total deals objects.

    HTTP methods:
    - GET


    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of total deals of dealer's customer.
    """

    serializer_class = TotalDealerPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsDealerOwner]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["amount"]
    filterset_class = DealerTotalDealsWithCustomerFilter

    def get_queryset(self):
        dealer_id = self.kwargs.get("pk")
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.total_purchases.all()
        except Dealer.DoesNotExist:
            return TotalDealerPurchase.objects.none()


class DealersHistoryWithSuppliersView(generics.ListAPIView):
    """
    Dealer's deals with supplier API endpoint.

    This endpoint provides a list of deals with supplier of specific dealer.
    Includes filtering and ordering dealer's deals with supplier objects.

    HTTP methods:
    - GET


    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of dealer's deals with supplier.
    """

    serializer_class = DealerDealsHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsDealerOwner]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["amount", "price_per_one", "date"]
    filterset_class = DealerDealsWithSupplierFilter

    def get_queryset(self):
        dealer_id = self.kwargs.get("pk")
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.history.all()
        except Dealer.DoesNotExist:
            return DealerDealsHistory.objects.none()


class DealersTotalHistoryWithSuppliersView(generics.ListAPIView):
    """
    Dealer's total deals with supplier API endpoint.

    This endpoint provides a list of total deals with supplier of specific dealer.
    Includes filtering and ordering dealer's total deals with suppliers objects.

    HTTP methods:
    - GET


    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of dealer's total deals with supplier.
    """

    serializer_class = TotalSupplierPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsDealerOwner]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["amount"]
    filterset_class = DealerTotalDealsWithSupplierFilter

    def get_queryset(self):
        dealer_id = self.kwargs.get("pk")
        try:
            dealer = Dealer.objects.get(pk=dealer_id)
            return dealer.orders_history.all()
        except Dealer.DoesNotExist:
            return TotalSupplierPurchase.objects.none()


class SuppliersHistoryWithDealersView(generics.ListAPIView):
    """
    Supplier's deals with dealer API endpoint.

    This endpoint provides a list of deals with dealer of specific supplier.
    Includes filtering and ordering supplier's deals objects.

    HTTP methods:
    - GET


    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of supplier's deals with dealer.
    """

    serializer_class = DealerDealsHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwner]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["amount", "price_per_one", "date"]
    filterset_class = SupplierDealsWithDealerFilter

    def get_queryset(self):
        supplier_id = self.kwargs.get("pk")
        try:
            supplier = Supplier.objects.get(pk=supplier_id)
            return supplier.dealer_history.all()
        except Supplier.DoesNotExist:
            return DealerDealsHistory.objects.none()


class SuppliersTotalPurchasesWithDealersView(generics.ListAPIView):
    """
    Supplier's total deals with dealers API endpoint.

    This endpoint provides a list of total deals with dealers of specific supplier.
    Includes filtering and ordering suppliers's total deals objects.

    HTTP methods:
    - GET


    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of supplier's total deals with dealer.
    """

    serializer_class = TotalSupplierPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwner]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["amount"]
    filterset_class = SupplierTotalDealsWithDealerFilter

    def get_queryset(self):
        supplier_id = self.kwargs.get("pk")
        try:
            supplier = Supplier.objects.get(pk=supplier_id)
            return supplier.total_purchases.all()
        except Supplier.DoesNotExist:
            return TotalSupplierPurchase.objects.none()
