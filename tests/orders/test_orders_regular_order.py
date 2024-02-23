from datetime import datetime, timedelta
import pytest

from ddf import G
from django.test.utils import CaptureQueriesContext
from django.db import connection

from cars.models import Car
from dealers.models import Dealer, DealerStockItem
from orders.models import CustomerDealsHistory
from orders.tasks import run_cars_purchase
from suppliers.models import Supplier, SupplierStockItem
from tests.conftest import parse_captured_queries_context


@pytest.fixture
def dealer_regular_order_data_without_marketing() -> dict:
    dealer = G(Dealer, balance=100_000)

    car1 = G(Car)
    car2 = G(Car)
    car3 = G(Car)
    dealer_stock_item1 = G(DealerStockItem, dealer=dealer, car=car1, amount=0)
    dealer_stock_item2 = G(DealerStockItem, dealer=dealer, car=car2, amount=20)
    _dealer_stock_item3 = G(DealerStockItem, dealer=dealer, car=car3, amount=5000)

    first_date = datetime.now() - timedelta(days=30)
    _deal_history_item = G(
        CustomerDealsHistory, dealer=dealer, car=car1, date=first_date
    )
    _deal_history_item = G(
        CustomerDealsHistory, dealer=dealer, car=car2, date=first_date
    )
    for _ in range(49):
        _deal_history_item = G(CustomerDealsHistory, dealer=dealer, car=car1)
        _deal_history_item = G(CustomerDealsHistory, dealer=dealer, car=car2)

    supplier1 = G(Supplier)
    _supplier1_stock_item1 = G(
        SupplierStockItem, car=car1, amount=999999, price_per_one=1000
    )
    _supplier1_stock_item2 = G(
        SupplierStockItem, car=car2, amount=999999, price_per_one=2000
    )

    supplier2 = G(Supplier)
    _supplier2_stock_item1 = G(
        SupplierStockItem, car=car1, amount=999999, price_per_one=5000
    )
    _supplier3_stock_item2 = G(
        SupplierStockItem, car=car2, amount=999999, price_per_one=5000
    )
    _supplier3_stock_item3 = G(
        SupplierStockItem, car=car3, amount=999999, price_per_one=5000
    )

    return {
        "dealer": dealer,
        "car1": car1,
        "car2": car2,
        "car3": car3,
        "dealer_stock_item1": dealer_stock_item1,
        "dealer_stock_item2": dealer_stock_item2,
    }


@pytest.mark.django_db
class TestRegularOrder:
    def test_dealer_regular_purchase_handler_no_marketing(
        self, dealer_regular_order_data_without_marketing
    ):
        """
        Test regular purchasing for dealer without any marketing events.
        """
        data = dealer_regular_order_data_without_marketing
        with CaptureQueriesContext(connection) as ctx:
            run_cars_purchase(data["dealer"].pk)

            q_select, q_update, q_insert, q_len = parse_captured_queries_context(ctx)
            assert q_select <= 16
            assert q_update <= 8
            assert q_insert <= 4
            assert q_len <= 36

        dealer = dealer_regular_order_data_without_marketing["dealer"]
        dealer.refresh_from_db()
        assert dealer.balance == 29000

        stock1 = data["dealer_stock_item1"]
        stock1.refresh_from_db()
        assert data["dealer_stock_item1"].amount == 37

        stock2 = data["dealer_stock_item2"]
        stock2.refresh_from_db()
        assert data["dealer_stock_item2"].amount == 37
