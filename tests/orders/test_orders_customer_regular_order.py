import pytest

from ddf import G
from django.test.utils import CaptureQueriesContext
from django.db import connection

from cars.models import Car
from customers.models import Customer
from dealers.models import Dealer, DealerStockItem
from orders.tasks import run_customer_purchase_with_random_car
from tests.conftest import parse_captured_queries_context


@pytest.fixture
def customer_regular_order() -> dict:
    """
    Fixture for customer regular orders
    """
    customer = G(Customer, balance=5_000)

    choosed_car = G(Car)
    car2 = G(Car)

    dealer1 = G(Dealer, balance=30_000, is_active=True)
    dealer1_stock_item1 = G(
        DealerStockItem, dealer=dealer1, car=choosed_car, amount=40, price_per_one=1000
    )
    _dealer1_stock_item2 = G(
        DealerStockItem, dealer=dealer1, car=car2, amount=50, price_per_one=2000
    )

    dealer2 = G(Dealer, balance=50_000)
    _dealer2_stock_item1 = G(
        DealerStockItem, dealer=dealer2, car=choosed_car, amount=60, price_per_one=5000
    )
    _dealer3_stock_item2 = G(
        DealerStockItem, dealer=dealer2, car=car2, amount=40, price_per_one=5000
    )

    return {
        "customer": customer,
        "dealer1": dealer1,
        "dealer1_stock_item1": dealer1_stock_item1,
        "max_price": 1000,
        "choosed_car": choosed_car,
        "car2": car2,
    }


@pytest.mark.django_db
class TestRegularOrder:
    def test_customer_regular_order(self, customer_regular_order):
        """
        Test regular purchasing for customers.
        """
        data = customer_regular_order
        with CaptureQueriesContext(connection) as ctx:
            run_customer_purchase_with_random_car(
                data["customer"].pk, data["choosed_car"].pk, data["max_price"]
            )

            q_select, q_update, q_insert, q_len = parse_captured_queries_context(ctx)
            assert q_select <= 9
            assert q_update <= 3
            assert q_insert <= 3
            assert q_len <= 19

        dealer = data["dealer1"]
        dealer.refresh_from_db()
        customer = data["customer"]
        customer.refresh_from_db()

        assert customer.balance == 4000
        assert dealer.balance == 31000

        assert data["choosed_car"] in customer.cars.all()

        stock1 = data["dealer1_stock_item1"]
        stock1.refresh_from_db()
        assert stock1.amount == 39
