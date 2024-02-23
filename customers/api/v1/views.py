from rest_framework import generics, mixins, viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from cars.api.v1.views import CarFiltersMixin
from customers.filters import CustomerFilter
from cars.filters import CarFilter
from customers.permissions import IsCustomerOwner
from common.permissions import IsProfileOwnerOrReadOnly
from orders.api.v1.serializers import CustomerDealsHistorySerializer
from orders.filters import CustomerDealsHistoryFilter
from orders.models import CustomerDealsHistory
from customers.api.v1.serializers import CustomerOwnerSerializer, CustomerSerializer
from customers.models import Customer
from cars.api.v1.serializers import CarSerializer
from cars.models import Car
from users.models import UserProfile


class CustomerAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Customer API endpoint.

    This endpoint provides Create, Retrieve, Update operations for customers.
    Includes filtering and ordering customer objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH


    Request parameters:
    - id (path parameter, optional)

    Actions:
    -POST : Create a new customer entry.
    -GET : Retrieve a list of all customers
    -GET : Retrieve a customer's detail by ID
    -PUT/PATCH : Update customer's data by ID
    """

    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["balance"]
    filterset_class = CustomerFilter

    def get_serializer_class(self):
        """
        Function to get serializer class based on request user.
        """
        if self.request.user.is_staff or (
            "pk" in self.kwargs
            and self.request.user.role == UserProfile.CUSTOMER
            and self.request.user.customer_profile.pk == int(self.kwargs.get("pk"))
        ):
            return CustomerOwnerSerializer
        return CustomerSerializer


class CustomerCarsListAPIView(CarFiltersMixin, generics.ListAPIView):
    """
    Customer's cars API endpoint.

    This endpoint provides a list of cars of specific customer.
    Includes filtering and ordering customer's car objects.

    HTTP methods:
    - GET


    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all customer's cars
    """

    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOwner]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarFilter

    def get_queryset(self):
        customer_id = self.kwargs["pk"]
        try:
            customer = Customer.objects.get(pk=customer_id)
            return customer.cars.all()
        except Customer.DoesNotExist:
            return Car.objects.none()


class CustomerOrdersHistoryListAPIView(generics.ListAPIView):
    """
    Customer's orders history API endpoint.

    This endpoint provides a list of customer's orders.
    Includes filtering and ordering customer order objects.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)

    Actions:
    -GET : Retrieve a list of all customer's orders
    """

    serializer_class = CustomerDealsHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOwner]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["price_per_one", "date"]
    filterset_class = CustomerDealsHistoryFilter

    def get_queryset(self):
        customer_id = self.kwargs["pk"]
        try:
            customer = Customer.objects.get(pk=customer_id)
            return customer.history.all()
        except Customer.DoesNotExist:
            return CustomerDealsHistory.objects.none()
