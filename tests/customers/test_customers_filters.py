import pytest
from ddf import G
from customers.api.v1.serializers import CustomerSerializer

from customers.models import Customer
from orders.models import CustomerDealsHistory


@pytest.fixture
@pytest.mark.django_db
def customers_data():
    """
    Fixture with customers data to check filters.
    """
    customer1 = G(Customer, balance=2_000, is_active=True, place="CA")
    customer2 = G(Customer, balance=3_000, is_active=False, place="US")
    customer3 = G(Customer, balance=1_000, is_active=True, place="CA")
    customer4 = G(Customer, balance=4_000, is_active=False, place="US")

    return {
        "customer1": customer1,
        "customer2": customer2,
        "customer3": customer3,
        "customer4": customer4,
    }


@pytest.mark.parametrize(
    "customer_keys, query_param, query_value",
    [
        (
            ["customer3", "customer1", "customer2", "customer4"],
            "ordering",
            "balance",
        ),
        (
            ["customer4", "customer2", "customer1", "customer3"],
            "ordering",
            "-balance",
        ),
        (["customer1", "customer3"], "is_active", True),
        (["customer2", "customer4"], "is_active", False),
        (["customer1", "customer3"], "place", "CA"),
    ],
)
@pytest.mark.django_db
def test_customers_filters(
    api_client,
    customer_keys,
    query_param,
    query_value,
    customers_data,
):
    """
    Test customers filters.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get("/api/v1/customers/", data=data, format="json")
    serializer_data = CustomerSerializer(
        [customers_data[key] for key in customer_keys],
        many=True,
    ).data

    assert response.data == serializer_data


@pytest.fixture
@pytest.mark.django_db
def customers_orders_data():
    """
    Fixture with customers orders data to check filters.
    """
    customer = G(Customer)
    order1 = G(CustomerDealsHistory, customer=customer, price_per_one=1_000)
    order2 = G(CustomerDealsHistory, customer=customer, price_per_one=5_000)
    order3 = G(CustomerDealsHistory, customer=customer, price_per_one=2_000)
    order4 = G(CustomerDealsHistory, customer=customer, price_per_one=10_000)
    return {
        "order1": order1,
        "order2": order2,
        "order3": order3,
        "order4": order4,
        "customer": customer,
    }


@pytest.mark.parametrize(
    "orders_keys, query_param, query_value",
    [
        (["order1", "order2", "order3", "order4"], "ordering", "date"),
        (["order4", "order3", "order2", "order1"], "ordering", "-date"),
        (["order1", "order3", "order2", "order4"], "ordering", "price_per_one"),
        (["order4", "order2", "order3", "order1"], "ordering", "-price_per_one"),
    ],
)
@pytest.mark.django_db
def test_customers_orders_filters(
    api_client,
    orders_keys,
    query_param,
    query_value,
    customers_orders_data,
):
    """
    Test customers' orders filters.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get(
        f"/api/v1/customers/{customers_orders_data['customer'].pk}/purchase-history",
        data=data,
        format="json",
    )

    from orders.api.v1.serializers import CustomerDealsHistorySerializer

    serializer_data = CustomerDealsHistorySerializer(
        [customers_orders_data[key] for key in orders_keys],
        many=True,
    ).data

    assert response.data == serializer_data
