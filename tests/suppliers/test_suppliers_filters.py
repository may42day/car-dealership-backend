from datetime import datetime
import pytest
from ddf import G
from suppliers.api.v1.serializers import SupplierSerializer, SupplierStockItemSerializer

from suppliers.models import Supplier, SupplierStockItem


@pytest.fixture
@pytest.mark.django_db
def suppliers_data():
    """
    Fixture with suppliers data to check filters.
    """
    date1 = datetime(2023, 1, 1).date()
    date2 = datetime(2023, 4, 4).date()
    date3 = datetime(2023, 8, 8).date()
    date4 = datetime(2023, 12, 12).date()
    supplier1 = G(Supplier, foundation_date=date1, balance=1_500_000, place="US")
    supplier2 = G(Supplier, foundation_date=date2, balance=1_000_000, place="US")
    supplier3 = G(Supplier, foundation_date=date3, balance=2_000_000, place="CA")
    supplier4 = G(Supplier, foundation_date=date4, balance=2_500_000, place="CA")

    return {
        "supplier1": supplier1,
        "supplier2": supplier2,
        "supplier3": supplier3,
        "supplier4": supplier4,
    }


@pytest.mark.parametrize(
    "suppliers_profile_keys, query_param, query_value",
    [
        (
            ["supplier1", "supplier2", "supplier3", "supplier4"],
            "ordering",
            "foundation_date",
        ),
        (
            ["supplier4", "supplier3", "supplier2", "supplier1"],
            "ordering",
            "-foundation_date",
        ),
        (["supplier2", "supplier1", "supplier3", "supplier4"], "ordering", "balance"),
        (["supplier4", "supplier3", "supplier1", "supplier2"], "ordering", "-balance"),
        (["supplier1", "supplier2"], "foundation_date__lt", "2023-06-06"),
        (["supplier3", "supplier4"], "foundation_date__gt", "2023-06-06"),
        (["supplier1", "supplier2"], "place", "US"),
        (["supplier3", "supplier4"], "place", "CA"),
    ],
)
@pytest.mark.django_db
def test_suppliers_filters(
    api_client,
    suppliers_profile_keys,
    query_param,
    query_value,
    suppliers_data,
):
    """
    Tests suppliers filters.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get(
        f"/api/v1/suppliers/",
        data=data,
        format="json",
    )

    serializer_data = SupplierSerializer(
        [suppliers_data[key] for key in suppliers_profile_keys],
        many=True,
    ).data

    assert response.data == serializer_data


@pytest.fixture
@pytest.mark.django_db
def suppliers_stock_data():
    """
    Fixture with suppliers stock item data to check filters.
    """
    supplier = G(Supplier)
    supplier_stock1 = G(
        SupplierStockItem, supplier=supplier, price_per_one=2_000, amount=10
    )
    supplier_stock2 = G(
        SupplierStockItem, supplier=supplier, price_per_one=1_000, amount=20
    )
    supplier_stock3 = G(
        SupplierStockItem, supplier=supplier, price_per_one=4_000, amount=30
    )
    supplier_stock4 = G(
        SupplierStockItem, supplier=supplier, price_per_one=3_000, amount=40
    )

    return {
        "supplier": supplier,
        "stock1": supplier_stock1,
        "stock2": supplier_stock2,
        "stock3": supplier_stock3,
        "stock4": supplier_stock4,
    }


@pytest.mark.parametrize(
    "suppliers_stock_keys, query_param, query_value",
    [
        (["stock2", "stock1", "stock4", "stock3"], "ordering", "price_per_one"),
        (["stock3", "stock4", "stock1", "stock2"], "ordering", "-price_per_one"),
        (["stock1", "stock2", "stock3", "stock4"], "ordering", "amount"),
        (["stock4", "stock3", "stock2", "stock1"], "ordering", "-amount"),
    ],
)
@pytest.mark.django_db
def test_supplier_stock_filters(
    api_client,
    suppliers_stock_keys,
    query_param,
    query_value,
    suppliers_stock_data,
):
    """
    Tests suppliers stock item filters.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get(
        f"/api/v1/suppliers/stock/",
        data=data,
        format="json",
    )

    serializer_data = SupplierStockItemSerializer(
        [suppliers_stock_data[key] for key in suppliers_stock_keys],
        many=True,
    ).data

    assert response.data == serializer_data
