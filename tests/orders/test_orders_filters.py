from datetime import datetime
import pytest
from ddf import G
import pytz
from customers.models import Customer
from dealers.models import Dealer

from orders.models import (
    CustomerDealsHistory,
    CustomerOffer,
    DealerDealsHistory,
    DealerOffer,
    TotalDealerPurchase,
    TotalSupplierPurchase,
)
from suppliers.models import Supplier


@pytest.mark.django_db
def deals_history(model):
    """
    Function to create deals history data for specific model.
    """
    date1 = datetime(2023, 1, 1, tzinfo=pytz.UTC)
    date2 = datetime(2023, 3, 3, tzinfo=pytz.UTC)
    date3 = datetime(2023, 5, 5, tzinfo=pytz.UTC)
    date4 = datetime(2023, 7, 7, tzinfo=pytz.UTC)

    dealer = G(Dealer, id=99999)
    if model is CustomerDealsHistory:
        customer = G(Customer, id=99999)
        deal1 = G(
            model,
            amount=100,
            price_per_one=1_000,
            date=date1,
            dealer=dealer,
            customer=customer,
        )
        deal2 = G(
            model,
            amount=200,
            price_per_one=2_000,
            date=date2,
            dealer=dealer,
            customer=customer,
        )
        deal3 = G(
            model,
            amount=300,
            price_per_one=3_000,
            date=date3,
            dealer=dealer,
            customer=customer,
        )
        deal4 = G(
            model,
            amount=400,
            price_per_one=4_000,
            date=date4,
            dealer=dealer,
            customer=customer,
        )
    elif model is DealerDealsHistory:
        supplier = G(Supplier, id=99999)
        deal1 = G(
            model,
            amount=100,
            price_per_one=1_000,
            date=date1,
            dealer=dealer,
            supplier=supplier,
        )
        deal2 = G(
            model,
            amount=200,
            price_per_one=2_000,
            date=date2,
            dealer=dealer,
            supplier=supplier,
        )
        deal3 = G(
            model,
            amount=300,
            price_per_one=3_000,
            date=date3,
            dealer=dealer,
            supplier=supplier,
        )
        deal4 = G(
            model,
            amount=400,
            price_per_one=4_000,
            date=date4,
            dealer=dealer,
            supplier=supplier,
        )
    return {
        "deal1": deal1,
        "deal2": deal2,
        "deal3": deal3,
        "deal4": deal4,
        "instance_id": 99999,
    }


@pytest.fixture
def customer_deals_history():
    """
    Fixture to create customers deals data to check filters.
    """
    from orders.api.v1.serializers import CustomerDealsHistorySerializer

    data = deals_history(CustomerDealsHistory)
    data["serializer"] = CustomerDealsHistorySerializer
    return data


@pytest.fixture
def dealer_deals_history():
    """
    Fixture to create dealers deals data to check filters.
    """
    from orders.api.v1.serializers import DealerDealsHistorySerializer

    data = deals_history(DealerDealsHistory)
    data["serializer"] = DealerDealsHistorySerializer
    return data


@pytest.mark.parametrize(
    "url, fixture_data_name",
    [
        (
            "/api/v1/orders/customers",
            "customer_deals_history",
        ),
        (
            "/api/v1/orders/dealers/{}/customers",
            "customer_deals_history",
        ),
        (
            "/api/v1/orders/dealers/{}/suppliers",
            "dealer_deals_history",
        ),
        (
            "/api/v1/orders/suppliers/{}/dealers",
            "dealer_deals_history",
        ),
    ],
)
@pytest.mark.parametrize(
    "fixture_dict_prefix, query_param, query_value",
    [
        (["1", "2", "3", "4"], "ordering", "price_per_one"),
        (["4", "3", "2", "1"], "ordering", "-price_per_one"),
        (["1", "2", "3", "4"], "ordering", "amount"),
        (["4", "3", "2", "1"], "ordering", "-amount"),
        (["1", "2", "3", "4"], "ordering", "date"),
        (["4", "3", "2", "1"], "ordering", "-date"),
        (["1", "2"], "price_per_one__lt", 2500),
        (["3", "4"], "price_per_one__gt", 2500),
        (["1", "2"], "amount__lt", 250),
        (["3", "4"], "amount__gt", 250),
        (["1", "2"], "date__lt", "2023-04-04"),
        (["3", "4"], "date__gt", "2023-04-04"),
    ],
)
@pytest.mark.django_db
def test_deals_history_filters(
    api_client,
    fixture_data_name,
    url,
    query_param,
    query_value,
    fixture_dict_prefix,
    request,
    customer_deals_history,
    dealer_deals_history,
):
    """
    TEsts customer, dealers, suppliers deals history.
    """
    data = {
        query_param: query_value,
    }
    dict_data = request.getfixturevalue(fixture_data_name)
    url = url.format(dict_data["instance_id"])
    response = api_client.get(url, data=data, format="json")

    serializer_data = dict_data["serializer"](
        [dict_data[f"deal{prefix}"] for prefix in fixture_dict_prefix],
        many=True,
    ).data

    assert response.data == serializer_data


@pytest.mark.django_db
def total_deals_history(model):
    """
    Function to create total deals data for specific model.
    """
    dealer = G(Dealer, id=99999)
    if model is TotalDealerPurchase:
        customer = G(Customer, id=99999)
        deal1 = G(model, amount=100, dealer=dealer, customer=customer)
        deal2 = G(model, amount=200, dealer=dealer, customer=customer)
        deal3 = G(model, amount=300, dealer=dealer, customer=customer)
        deal4 = G(model, amount=400, dealer=dealer, customer=customer)
    elif model is TotalSupplierPurchase:
        supplier = G(Supplier, id=99999)
        deal1 = G(model, amount=100, dealer=dealer, supplier=supplier)
        deal2 = G(model, amount=200, dealer=dealer, supplier=supplier)
        deal3 = G(model, amount=300, dealer=dealer, supplier=supplier)
        deal4 = G(model, amount=400, dealer=dealer, supplier=supplier)
    return {
        "total1": deal1,
        "total2": deal2,
        "total3": deal3,
        "total4": deal4,
        "instance_id": 99999,
    }


@pytest.fixture
def customer_total_deals_history():
    """
    Fixture to create customers total deals data to check filters.
    """
    from orders.api.v1.serializers import TotalDealerPurchaseSerializer

    data = total_deals_history(TotalDealerPurchase)
    data["serializer"] = TotalDealerPurchaseSerializer
    return data


@pytest.fixture
def dealer_total_deals_history():
    """
    Fixture to create dealers total deals data to check filters.
    """
    from orders.api.v1.serializers import TotalSupplierPurchaseSerializer

    data = total_deals_history(TotalSupplierPurchase)
    data["serializer"] = TotalSupplierPurchaseSerializer
    return data


@pytest.mark.parametrize(
    "url, fixture_data_name",
    [
        (
            "/api/v1/orders/dealers/{}/customers/total",
            "customer_total_deals_history",
        ),
        (
            "/api/v1/orders/dealers/{}/suppliers/total",
            "dealer_total_deals_history",
        ),
        (
            "/api/v1/orders/suppliers/{}/total/dealers",
            "dealer_total_deals_history",
        ),
    ],
)
@pytest.mark.parametrize(
    "fixture_dict_prefix, query_param, query_value",
    [
        (["1", "2", "3", "4"], "ordering", "amount"),
        (["4", "3", "2", "1"], "ordering", "-amount"),
        (["1", "2"], "amount__lt", 250),
        (["3", "4"], "amount__gt", 250),
    ],
)
@pytest.mark.django_db
def test_total_orders_filters(
    api_client,
    fixture_data_name,
    url,
    query_param,
    query_value,
    fixture_dict_prefix,
    request,
    customer_total_deals_history,
    dealer_total_deals_history,
):
    """
    Tests filters for total delas for customers, delaers and suppliers.
    """
    data = {
        query_param: query_value,
    }
    dict_data = request.getfixturevalue(fixture_data_name)
    url = url.format(dict_data["instance_id"])
    response = api_client.get(url, data=data, format="json")

    serializer_data = dict_data["serializer"](
        [dict_data[f"total{prefix}"] for prefix in fixture_dict_prefix],
        many=True,
    ).data

    assert response.data == serializer_data


@pytest.mark.django_db
def offers(model):
    """
    Function to create dict with offers for specific model.
    """
    offer1 = G(model, place="US", max_price=1_000, is_closed=True)
    offer2 = G(model, place="US", max_price=2_000, is_closed=True)
    offer3 = G(model, place="US", max_price=3_000, is_closed=False)
    offer4 = G(model, place="US", max_price=4_000, is_closed=False)

    return {
        "offer1": offer1,
        "offer2": offer2,
        "offer3": offer3,
        "offer4": offer4,
    }


@pytest.fixture
def customer_offers():
    """
    Fixture with customers offers data to check filters.
    """
    from orders.api.v1.serializers import CustomerOfferSerializer

    data = offers(CustomerOffer)
    data["serializer"] = CustomerOfferSerializer
    return data


@pytest.fixture
def dealer_offers():
    """
    Fixture with dealers offers data to check filters.
    """
    from orders.api.v1.serializers import DealerOfferSerializer

    data = offers(DealerOffer)
    data["serializer"] = DealerOfferSerializer
    return data


@pytest.mark.parametrize(
    "url, fixture_data_name",
    [
        (
            "/api/v1/orders/customers/offers",
            "customer_offers",
        ),
        (
            "/api/v1/orders/dealers/offers",
            "dealer_offers",
        ),
    ],
)
@pytest.mark.parametrize(
    "fixture_dict_prefix, query_param, query_value",
    [
        (["1", "2", "3", "4"], "ordering", "max_price"),
        (["4", "3", "2", "1"], "ordering", "-max_price"),
        (["1", "2"], "is_closed", True),
        (["3", "4"], "is_closed", False),
    ],
)
@pytest.mark.django_db
def test_offers_filters(
    api_client,
    fixture_data_name,
    url,
    query_param,
    query_value,
    fixture_dict_prefix,
    request,
    customer_offers,
    dealer_offers,
):
    """
    Tests offers filters dor dealers and customers.
    """
    data = {
        query_param: query_value,
    }
    dict_data = request.getfixturevalue(fixture_data_name)
    response = api_client.get(url, data=data, format="json")

    serializer_data = dict_data["serializer"](
        [dict_data[f"offer{prefix}"] for prefix in fixture_dict_prefix],
        many=True,
    ).data

    assert response.data == serializer_data
