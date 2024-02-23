from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError

from customers.models import Customer
from customers.permissions import IsCustomerOwner
from dealers.models import Dealer
from dealers.permissions import IsDealerOwner
from orders.models import CustomerDealsHistory, DealerDealsHistory
from stats.utils import get_filter_params
from suppliers.models import Supplier
from suppliers.permissions import IsSupplierOwner


class CustomerStatsView(APIView):
    """
    CustomerStats API endpoint.

    API to get diferent customer's statistics.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)
    - stats (query parameter)
    - start_date (query parameter, optional)
    - end_date (query parameter, optional)

    Actions:
    -GET : Get specific statistic based on query param.
    """

    permission_classes = [permissions.IsAuthenticated, IsCustomerOwner]

    def get(self, request, pk: int):
        customer = get_object_or_404(Customer, pk=pk)

        stats_type = request.query_params.get("stats")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        filter_params = get_filter_params("customer", customer, start_date, end_date)

        if stats_type == "bought_cars":
            amount = CustomerDealsHistory.objects.get_total_amount_of_cars(
                filter_params
            )
        elif stats_type == "spent_money":
            amount = CustomerDealsHistory.objects.get_total_cost(filter_params)
        else:
            raise ValidationError("Get parameter 'stats' is required.")

        return Response({"amount": amount}, status=status.HTTP_200_OK)


class DealerStatsView(APIView):
    """
    DealerStats API endpoint.

    API to get diferent dealers's statistics.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)
    - stats (query parameter)
    - start_date (query parameter, optional)
    - end_date (query parameter, optional)

    Actions:
    -GET : Get specific statistic based on query param.
    """

    permission_classes = [permissions.IsAuthenticated, IsDealerOwner]

    def get(self, request, pk: int):
        dealer = get_object_or_404(Dealer, pk=pk)

        stats_type = request.query_params.get("stats")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        filter_params = get_filter_params("dealer", dealer, start_date, end_date)

        if stats_type == "amount_bought_cars":
            amount = DealerDealsHistory.objects.get_total_amount_of_cars(filter_params)
        elif stats_type == "spent_money":
            amount = DealerDealsHistory.objects.get_total_cost(filter_params)
        elif stats_type == "amount_unique_clients":
            amount = CustomerDealsHistory.objects.get_amount_of_unique_clients(
                filter_params
            )
        elif stats_type == "amount_sold_cars":
            amount = CustomerDealsHistory.objects.get_total_amount_of_cars(
                filter_params
            )
        elif stats_type == "amount_sold_unique_cars":
            amount = CustomerDealsHistory.objects.get_amount_of_sold_unique_cars(
                filter_params
            )
        elif stats_type == "revenue":
            amount = CustomerDealsHistory.objects.get_total_cost(filter_params)
        else:
            raise ValidationError("Get parameter 'stats' is required.")

        return Response({"amount": amount}, status=status.HTTP_200_OK)


class SupplierStatsView(APIView):
    """
    SupplierStats API endpoint.

    API to get diferent customer's statistics.

    HTTP methods:
    - GET

    Request parameters:
    - id (path parameter)
    - stats (query parameter)
    - start_date (query parameter, optional)
    - end_date (query parameter, optional)

    Actions:
    -GET : Get specific statistic based on query param.
    """

    permission_classes = [permissions.IsAuthenticated, IsSupplierOwner]

    def get(self, request, pk: int):
        supplier = get_object_or_404(Supplier, pk=pk)

        stats_type = request.query_params.get("stats")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        filter_params = get_filter_params("supplier", supplier, start_date, end_date)

        if stats_type == "amount_unique_clients":
            amount = DealerDealsHistory.objects.get_amount_of_unique_clients(
                filter_params
            )
        elif stats_type == "amount_sold_cars":
            amount = DealerDealsHistory.objects.get_total_amount_of_cars(filter_params)
        elif stats_type == "amount_sold_unique_cars":
            amount = DealerDealsHistory.objects.get_amount_of_sold_unique_cars(
                filter_params
            )
        elif stats_type == "revenue":
            amount = DealerDealsHistory.objects.get_total_cost(filter_params)
        else:
            raise ValidationError("Get parameter 'stats' is required.")

        return Response({"amount": amount}, status=status.HTTP_200_OK)
