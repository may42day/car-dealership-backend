from datetime import datetime
import pytz
from rest_framework import status
from django.utils import timezone
from ddf import G
import pytest

from orders.models import CustomerDealsHistory, DealerDealsHistory
from customers.models import Customer
from dealers.models import Dealer
from cars.models import Car


@pytest.fixture
def init_customer_data(specific_customer):
    """
    Function to initialize customer's deals.
    """
    date1 = datetime(2023, 5, 5, tzinfo=pytz.UTC)
    date2 = datetime(2023, 10, 10, tzinfo=pytz.UTC)
    deal1 = G(
        CustomerDealsHistory,
        customer=specific_customer,
        amount=1,
        price_per_one=5_000,
        date=date1,
    )
    deal2 = G(
        CustomerDealsHistory,
        customer=specific_customer,
        amount=1,
        price_per_one=5_000,
        date=date2,
    )


@pytest.mark.parametrize(
    "result, querydata",
    [
        (10_000, {"stats": "spent_money"}),
        (
            5_000,
            {
                "stats": "spent_money",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (
            5_000,
            {
                "stats": "spent_money",
                "start_date": "2023-06-06",
            },
        ),
        (
            5_000,
            {
                "stats": "spent_money",
                "end_date": "2023-06-06",
            },
        ),
        (2, {"stats": "bought_cars"}),
        (
            1,
            {
                "stats": "bought_cars",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (
            1,
            {
                "stats": "bought_cars",
                "end_date": "2023-06-06",
            },
        ),
        (
            1,
            {
                "stats": "bought_cars",
                "start_date": "2023-06-06",
            },
        ),
    ],
)
@pytest.mark.django_db
def test_stats_customer(
    api_client, result, querydata, specific_customer, init_customer_data
):
    """
    Test to check customer stats API with diferent query params.
    """
    api_client.force_authenticate(user=specific_customer.user_profile)
    response = api_client.get(
        f"/api/v1/stats/customers/{specific_customer.pk}", data=querydata
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["amount"] == result


@pytest.fixture
def init_dealer_data(specific_dealer):
    """
    Function to initialize dealers's deals.
    """
    date1 = datetime(2023, 5, 5, tzinfo=pytz.UTC)
    date2 = datetime(2023, 10, 10, tzinfo=pytz.UTC)

    car1 = G(Car)
    car2 = G(Car)

    customer1 = G(Customer)
    customer2 = G(Customer)

    deal1 = G(
        CustomerDealsHistory,
        dealer=specific_dealer,
        customer=customer1,
        car=car1,
        amount=1,
        price_per_one=5_000,
        date=date1,
    )
    deal2 = G(
        CustomerDealsHistory,
        dealer=specific_dealer,
        customer=customer2,
        car=car2,
        amount=1,
        price_per_one=5_000,
        date=date2,
    )

    supplier_deal1 = G(
        DealerDealsHistory,
        dealer=specific_dealer,
        car=car1,
        amount=2,
        price_per_one=10_000,
        date=date1,
    )
    supplier_deal2 = G(
        DealerDealsHistory,
        dealer=specific_dealer,
        car=car2,
        amount=2,
        price_per_one=10_000,
        date=date2,
    )


@pytest.mark.parametrize(
    "result, querydata",
    [
        (4, {"stats": "amount_bought_cars"}),
        (
            2,
            {
                "stats": "amount_bought_cars",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (40_000, {"stats": "spent_money"}),
        (
            20_000,
            {
                "stats": "spent_money",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (2, {"stats": "amount_unique_clients"}),
        (
            1,
            {
                "stats": "amount_unique_clients",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (2, {"stats": "amount_sold_cars"}),
        (
            1,
            {
                "stats": "amount_sold_cars",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (2, {"stats": "amount_sold_unique_cars"}),
        (
            1,
            {
                "stats": "amount_sold_unique_cars",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (10_000, {"stats": "revenue"}),
        (
            5_000,
            {"stats": "revenue", "start_date": "2023-01-01", "end_date": "2023-06-06"},
        ),
    ],
)
@pytest.mark.django_db
def test_stats_dealer(api_client, result, querydata, specific_dealer, init_dealer_data):
    """
    Test to check dealers stats API with diferent query params.
    """
    api_client.force_authenticate(user=specific_dealer.user_profile)
    response = api_client.get(
        f"/api/v1/stats/dealers/{specific_dealer.pk}", data=querydata
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["amount"] == result


@pytest.fixture
def init_supplier_data(specific_supplier):
    """
    Function to initialize supplier's deals.
    """
    date1 = datetime(2023, 5, 5, tzinfo=pytz.UTC)
    date2 = datetime(2023, 10, 10, tzinfo=pytz.UTC)

    car1 = G(Car)
    car2 = G(Car)

    dealer1 = G(Dealer)
    dealer2 = G(Dealer)

    deal1 = G(
        DealerDealsHistory,
        supplier=specific_supplier,
        dealer=dealer1,
        car=car1,
        amount=2,
        price_per_one=10_000,
        date=date1,
    )
    deal2 = G(
        DealerDealsHistory,
        supplier=specific_supplier,
        dealer=dealer2,
        car=car2,
        amount=2,
        price_per_one=10_000,
        date=date2,
    )


@pytest.mark.parametrize(
    "result, querydata",
    [
        (2, {"stats": "amount_unique_clients"}),
        (
            1,
            {
                "stats": "amount_unique_clients",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (4, {"stats": "amount_sold_cars"}),
        (
            2,
            {
                "stats": "amount_sold_cars",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (2, {"stats": "amount_sold_unique_cars"}),
        (
            1,
            {
                "stats": "amount_sold_unique_cars",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            },
        ),
        (40_000, {"stats": "revenue"}),
        (
            20_000,
            {"stats": "revenue", "start_date": "2023-01-01", "end_date": "2023-06-06"},
        ),
    ],
)
@pytest.mark.django_db
def test_stats_supplier(
    api_client, specific_supplier, init_supplier_data, result, querydata
):
    """
    Test to check suppliers stats API with diferent query params.
    """
    api_client.force_authenticate(user=specific_supplier.user_profile)
    response = api_client.get(
        f"/api/v1/stats/suppliers/{specific_supplier.pk}", data=querydata
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["amount"] == result
