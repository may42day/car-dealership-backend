from datetime import datetime
import pytest
from ddf import G
from dealers.api.v1.serializers import DealerSerializer, DealerStockItemSerializer

from dealers.models import Dealer, DealerStockItem


@pytest.fixture
@pytest.mark.django_db
def dealers_data():
    """
    Function to create delaers data to check filters.
    """
    date1 = datetime(2023, 1, 1).date()
    date2 = datetime(2023, 4, 4).date()
    date3 = datetime(2023, 8, 8).date()
    date4 = datetime(2023, 12, 12).date()
    dealer1 = G(Dealer, foundation_date=date1, balance=1_500_000, place="US")
    dealer2 = G(Dealer, foundation_date=date2, balance=1_000_000, place="US")
    dealer3 = G(Dealer, foundation_date=date3, balance=2_000_000, place="CA")
    dealer4 = G(Dealer, foundation_date=date4, balance=2_500_000, place="CA")

    return {
        "dealer1": dealer1,
        "dealer2": dealer2,
        "dealer3": dealer3,
        "dealer4": dealer4,
    }


@pytest.mark.parametrize(
    "dealers_profile_keys, query_param, query_value",
    [
        (["dealer1", "dealer2", "dealer3", "dealer4"], "ordering", "foundation_date"),
        (["dealer4", "dealer3", "dealer2", "dealer1"], "ordering", "-foundation_date"),
        (["dealer2", "dealer1", "dealer3", "dealer4"], "ordering", "balance"),
        (["dealer4", "dealer3", "dealer1", "dealer2"], "ordering", "-balance"),
        (["dealer1", "dealer2"], "foundation_date__lt", "2023-06-06"),
        (["dealer3", "dealer4"], "foundation_date__gt", "2023-06-06"),
        (["dealer1", "dealer2"], "place", "US"),
        (["dealer3", "dealer4"], "place", "CA"),
    ],
)
@pytest.mark.django_db
def test_dealers_filters(
    api_client,
    dealers_profile_keys,
    query_param,
    query_value,
    dealers_data,
):
    """
    Tests dealers filters.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get(
        f"/api/v1/dealers/",
        data=data,
        format="json",
    )

    serializer_data = DealerSerializer(
        [dealers_data[key] for key in dealers_profile_keys],
        many=True,
    ).data

    assert response.data == serializer_data


@pytest.fixture
@pytest.mark.django_db
def dealers_stock_data():
    """
    Function to create delaers stock item data to check filters.
    """
    dealer = G(Dealer)
    dealer_stock1 = G(DealerStockItem, dealer=dealer, price_per_one=2_000, amount=10)
    dealer_stock2 = G(DealerStockItem, dealer=dealer, price_per_one=1_000, amount=20)
    dealer_stock3 = G(DealerStockItem, dealer=dealer, price_per_one=4_000, amount=30)
    dealer_stock4 = G(DealerStockItem, dealer=dealer, price_per_one=3_000, amount=40)

    return {
        "dealer": dealer,
        "stock1": dealer_stock1,
        "stock2": dealer_stock2,
        "stock3": dealer_stock3,
        "stock4": dealer_stock4,
    }


@pytest.mark.parametrize(
    "dealers_stock_keys, query_param, query_value",
    [
        (["stock2", "stock1", "stock4", "stock3"], "ordering", "price_per_one"),
        (["stock3", "stock4", "stock1", "stock2"], "ordering", "-price_per_one"),
        (["stock1", "stock2", "stock3", "stock4"], "ordering", "amount"),
        (["stock4", "stock3", "stock2", "stock1"], "ordering", "-amount"),
    ],
)
@pytest.mark.django_db
def test_dealer_stock_filters(
    api_client,
    dealers_stock_keys,
    query_param,
    query_value,
    dealers_stock_data,
):
    """
    Tests filters for delaers' stock items.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get(
        f"/api/v1/dealers/stock/",
        data=data,
        format="json",
    )

    serializer_data = DealerStockItemSerializer(
        [dealers_stock_data[key] for key in dealers_stock_keys],
        many=True,
    ).data

    assert response.data == serializer_data
