from rest_framework import generics, viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from common.mixins import SupplierOwnerMixin

from common.permissions import IsProfileOwnerOrReadOnly
from marketing.filters import SupplierDiscountFilter, SupplierMarketingCampaignFilter
from marketing.models import SupplierDiscount, SupplierMarketingCampaign
from orders.filters import DealerTotalDealsWithSupplierFilter
from orders.models import TotalSupplierPurchase
from suppliers.api.v1.serializers import (
    SupplierOwnerSerializer,
    SupplierSerializer,
    SupplierStockItemSerializer,
)
from suppliers.filters import SupplierFilter, SupplierStockFilter
from suppliers.models import Supplier, SupplierStockItem
from marketing.api.v1.serializers import (
    SupplierDiscountSerializer,
    SupplierMarketingCampaignSerializer,
)
from orders.api.v1.serializers import (
    TotalSupplierPurchaseSerializer,
)
from suppliers.permissions import IsSupplierOwner, IsSupplierOwnerOrReadOnly
from users.models import UserProfile


class SupplierAPIView(viewsets.ModelViewSet):
    """
    Supplier endpoint.

    This endpoint provides CRUD operations for supplier.
    Includes filtering and ordering Supplier objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new supplier's entry.
    -GET : Retrieve a list of all suppliers
    -GET : Retrieve a supplier's detail by supplier ID.
    -PUT/PATCH : Update supplier's data by ID.
    """

    queryset = Supplier.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["foundation_date", "balance"]
    filterset_class = SupplierFilter

    def get_serializer_class(self):
        """
        Function to get serializer class based on request user.
        """
        if self.request.user.is_staff or (
            "pk" in self.kwargs
            and self.request.user.role == UserProfile.SUPPLIER
            and self.request.user.supplier.pk == int(self.kwargs.get("pk"))
        ):
            return SupplierOwnerSerializer
        return SupplierSerializer


class SuppliersClientsListAPIView(generics.ListAPIView):
    """
    Suppliers' clients' total purchases API endpoint.

    This endpoint provides a list of supplier's clients with their total purchases.
    Includes filtering TotalSupplierPurchase objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all supplier's clinets total purchases.
    """

    serializer_class = TotalSupplierPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwner]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DealerTotalDealsWithSupplierFilter

    def get_queryset(self):
        supplier_id = self.kwargs["pk"]
        try:
            supplier = Supplier.objects.get(pk=supplier_id)
            return supplier.total_purchases.all()
        except Supplier.DoesNotExist:
            return TotalSupplierPurchase.objects.none()


class SupplierStockAPIView(SupplierOwnerMixin, viewsets.ModelViewSet):
    """
    Supplier stock endpoint.

    This endpoint provides CRUD operations for supplier's stock.
    Includes filtering and ordering supplier's stock item objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new supplier's stock item entry.
    -GET : Retrieve a list of all supplier' stock items.
    -GET : Retrieve a supplier's stock item detail by supplier ID.
    -PUT/PATCH : Update supplier's stock item data by ID.
    """

    queryset = SupplierStockItem.objects.all()
    serializer_class = SupplierStockItemSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsSupplierOwnerOrReadOnly,
    ]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["price_per_one", "amount"]
    filterset_class = SupplierStockFilter


class SupplierDiscountListAPIView(generics.ListAPIView):
    """
    Suppliers' discounts API endpoint.

    This endpoint provides a list of supplier's discounts.
    Includes filtering and ordering supplier discounts objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all supplier's discounts.
    """

    serializer_class = SupplierDiscountSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["min_amount", "percentage"]
    filterset_class = SupplierDiscountFilter

    def get_queryset(self):
        supplier_id = self.kwargs["pk"]
        try:
            supplier = Supplier.objects.get(pk=supplier_id)
            return supplier.discounts.all()
        except Supplier.DoesNotExist:
            return SupplierDiscount.objects.none()


class SupplierMarketingListAPIView(generics.ListAPIView):
    """
    Suppliers' marketing campaigns API endpoint.

    This endpoint provides a list of supplier's marketing campaigns.
    Includes filtering and ordering supplier marketing campaign objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all supplier's marketing campaigns.
    """

    serializer_class = SupplierMarketingCampaignSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["min_amount", "percentage"]
    filterset_class = SupplierMarketingCampaignFilter

    def get_queryset(self):
        supplier_id = self.kwargs["pk"]
        try:
            supplier = Supplier.objects.get(pk=supplier_id)
            return supplier.marketing_campaigns.all()
        except Supplier.DoesNotExist:
            return SupplierMarketingCampaign.objects.none()
