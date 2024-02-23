import pytest

from ddf import G
from django.test.utils import CaptureQueriesContext
from django.db import connection

from cars.models import Car
from dealers.models import DealerStockItem
from orders.tasks import check_cooperation_profitability
from suppliers.models import Supplier, SupplierStockItem
from tests.conftest import parse_captured_queries_context


@pytest.fixture
def init_dealers_data(specific_dealer) -> dict:
    """
    Initialize dealer's data to check cooperation profitability with suppliers
    """

    car1 = G(Car)
    car2 = G(Car)
    car3 = G(Car)
    car4 = G(Car)

    d_stock1 = G(DealerStockItem, car=car1, dealer=specific_dealer, is_active=True)
    d_stock2 = G(DealerStockItem, car=car2, dealer=specific_dealer, is_active=True)
    d_stock3 = G(DealerStockItem, car=car3, dealer=specific_dealer, is_active=True)

    supplier1 = G(Supplier)
    s1_stock1 = G(
        SupplierStockItem,
        supplier=supplier1,
        car=car1,
        amount=999999,
        price_per_one=1_000,
    )
    s1_stock2 = G(
        SupplierStockItem,
        supplier=supplier1,
        car=car2,
        amount=999999,
        price_per_one=5_000,
    )
    s1_stock3 = G(
        SupplierStockItem,
        supplier=supplier1,
        car=car3,
        amount=999999,
        price_per_one=5_000,
    )
    supplier2 = G(Supplier)
    s2_stock1 = G(
        SupplierStockItem,
        supplier=supplier2,
        car=car1,
        amount=999999,
        price_per_one=5_000,
    )
    s2_stock2 = G(
        SupplierStockItem,
        supplier=supplier2,
        car=car2,
        amount=999999,
        price_per_one=5_000,
    )
    s2_stock3 = G(
        SupplierStockItem,
        supplier=supplier2,
        car=car3,
        amount=999999,
        price_per_one=1_000,
    )
    supplier3 = G(Supplier)
    s3_stock1 = G(
        SupplierStockItem,
        supplier=supplier3,
        car=car1,
        amount=999999,
        price_per_one=5_000,
    )
    s3_stock2 = G(
        SupplierStockItem,
        supplier=supplier3,
        car=car2,
        amount=999999,
        price_per_one=5_000,
    )
    s3_stock3 = G(
        SupplierStockItem,
        supplier=supplier3,
        car=car3,
        amount=999999,
        price_per_one=5_000,
    )
    s3_stock4 = G(
        SupplierStockItem,
        supplier=supplier3,
        car=car4,
        amount=999999,
        price_per_one=1_000,
    )

    specific_dealer.suppliers.add(supplier3)
    return {
        "supplier1": supplier1,
        "supplier2": supplier2,
        "supplier3": supplier3,
    }


@pytest.mark.django_db
def test_check_cooperation_profitability(specific_dealer, init_dealers_data):
    """
    Test dealer cooperation profitability with suppliers task.
    """
    data = init_dealers_data
    with CaptureQueriesContext(connection) as ctx:
        check_cooperation_profitability(specific_dealer.pk)

        q_select, q_update, q_insert, q_len = parse_captured_queries_context(ctx)
        assert q_select <= 13
        assert q_update <= 0
        assert q_insert <= 1
        assert q_len <= 15

    specific_dealer.refresh_from_db()
    suppliers = specific_dealer.suppliers.all()
    assert data["supplier3"] not in suppliers
    assert data["supplier1"] in suppliers
    assert data["supplier2"] in suppliers
