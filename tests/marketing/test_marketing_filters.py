from datetime import datetime
import pytest
from ddf import G
from django.utils import timezone
import pytz
from marketing.api.v1.serializers import (
    DealerDiscountSerializer,
    DealerMarketingCampaignSerializer,
    SupplierDiscountSerializer,
    SupplierMarketingCampaignSerializer,
)

from marketing.models import (
    DealerDiscount,
    DealerMarketingCampaign,
    SupplierDiscount,
    SupplierMarketingCampaign,
)


@pytest.mark.django_db
def create_data(model):
    """
    Function to create marketing campaigns data for specific model.
    """
    start_date1 = datetime(2023, 1, 1, tzinfo=pytz.UTC)
    start_date2 = datetime(2023, 3, 3, tzinfo=pytz.UTC)
    start_date3 = datetime(2023, 5, 5, tzinfo=pytz.UTC)
    start_date4 = datetime(2023, 7, 7, tzinfo=pytz.UTC)

    end_date1 = datetime(2023, 2, 2, tzinfo=pytz.UTC)
    end_date2 = datetime(2023, 4, 4, tzinfo=pytz.UTC)
    end_date3 = datetime(2023, 6, 6, tzinfo=pytz.UTC)
    end_date4 = datetime(2023, 10, 10, tzinfo=pytz.UTC)

    marketing1 = G(
        model,
        percentage=10,
        start_date=start_date1,
        end_date=end_date1,
        name="TEST",
        description="description",
    )
    marketing2 = G(
        model,
        percentage=20,
        start_date=start_date2,
        end_date=end_date2,
        name="name",
        description="TEST",
    )
    marketing3 = G(
        model,
        percentage=30,
        start_date=start_date3,
        end_date=end_date3,
        name="name",
        description="description",
    )
    marketing4 = G(
        model,
        percentage=40,
        start_date=start_date4,
        end_date=end_date4,
        name="name",
        description="description",
    )

    return {
        "marketing1": marketing1,
        "marketing2": marketing2,
        "marketing3": marketing3,
        "marketing4": marketing4,
    }


@pytest.fixture
def dealers_marketing_data():
    """
    Function to create delaers marketing campaigns data to check filters.
    """
    return create_data(DealerMarketingCampaign)


@pytest.fixture
def suppliers_marketing_data():
    """
    Function to create suppliers marketing campaigns data to check filters.
    """
    return create_data(SupplierMarketingCampaign)


@pytest.mark.parametrize(
    "url, fixture_data_name, serializer",
    [
        (
            "/api/v1/marketing/dealers/campaigns/",
            "dealers_marketing_data",
            DealerMarketingCampaignSerializer,
        ),
        (
            "/api/v1/marketing/suppliers/campaigns/",
            "suppliers_marketing_data",
            SupplierMarketingCampaignSerializer,
        ),
    ],
)
@pytest.mark.parametrize(
    "fixture_dict_prefix, query_param, query_value",
    [
        (["1", "2"], "search", "TEST"),
        (["1", "2", "3", "4"], "ordering", "end_date"),
        (["4", "3", "2", "1"], "ordering", "-end_date"),
        (["1", "2", "3", "4"], "ordering", "start_date"),
        (["4", "3", "2", "1"], "ordering", "-start_date"),
        (["1", "2", "3", "4"], "ordering", "percentage"),
        (["4", "3", "2", "1"], "ordering", "-percentage"),
        (["2", "3", "4"], "start_date__gt", "2023-02-02"),
        (["1", "2", "3"], "start_date__lt", "2023-06-06"),
        (["2", "3", "4"], "end_date__gt", "2023-03-03"),
        (["1", "2", "3"], "end_date__lt", "2023-07-07"),
        (["1", "2"], "percentage__lt", 25),
        (["3", "4"], "percentage__gt", 25),
    ],
)
@pytest.mark.django_db
def test_marketing_campaigns_filters(
    api_client,
    fixture_data_name,
    url,
    query_param,
    query_value,
    fixture_dict_prefix,
    serializer,
    request,
    dealers_marketing_data,
    suppliers_marketing_data,
):
    """
    Tests marketing campaigns filters for dealers and suppliers.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get(url, data=data, format="json")
    dict_data = request.getfixturevalue(fixture_data_name)
    serializer_data = serializer(
        [dict_data[f"marketing{prefix}"] for prefix in fixture_dict_prefix],
        many=True,
    ).data

    assert response.data == serializer_data


@pytest.mark.django_db
def create_discount_data(model):
    """
    Function to create discounts data for specific model.
    """
    discount1 = G(model, min_amount=10, discount_type="CD", percentage=10)
    discount2 = G(model, min_amount=20, discount_type="CD", percentage=20)
    discount3 = G(model, min_amount=30, discount_type="BD", percentage=30)
    discount4 = G(model, min_amount=40, discount_type="BD", percentage=40)

    return {
        "discount1": discount1,
        "discount2": discount2,
        "discount3": discount3,
        "discount4": discount4,
    }


@pytest.fixture
def dealers_discount_data():
    """
    Function to create delaers discounts data to check filters.
    """
    return create_discount_data(DealerDiscount)


@pytest.fixture
def suppliers_discount_data():
    """
    Function to create suppliers discounts data to check filters.
    """
    return create_discount_data(SupplierDiscount)


@pytest.mark.parametrize(
    "url, fixture_data_name, serializer",
    [
        (
            "/api/v1/marketing/dealers/discounts/",
            "dealers_discount_data",
            DealerDiscountSerializer,
        ),
        (
            "/api/v1/marketing/suppliers/discounts/",
            "suppliers_discount_data",
            SupplierDiscountSerializer,
        ),
    ],
)
@pytest.mark.parametrize(
    "fixture_dict_prefix, query_param, query_value",
    [
        (["1", "2", "3", "4"], "ordering", "percentage"),
        (["4", "3", "2", "1"], "ordering", "-percentage"),
        (["1", "2", "3", "4"], "ordering", "min_amount"),
        (["4", "3", "2", "1"], "ordering", "-min_amount"),
        (["1", "2"], "percentage__lt", 25),
        (["3", "4"], "percentage__gt", 25),
        (["3", "4"], "min_amount__gt", 25),
        (["1", "2"], "min_amount__lt", 25),
        (["1", "2"], "discount_type", "CD"),
        (["3", "4"], "discount_type", "BD"),
    ],
)
@pytest.mark.django_db
def test_discount_filters(
    api_client,
    fixture_data_name,
    url,
    query_param,
    query_value,
    fixture_dict_prefix,
    serializer,
    request,
    dealers_discount_data,
    suppliers_discount_data,
):
    """
    Tests filters for dealers and suppliers discounts.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get(url, data=data, format="json")
    dict_data = request.getfixturevalue(fixture_data_name)
    serializer_data = serializer(
        [dict_data[f"discount{prefix}"] for prefix in fixture_dict_prefix],
        many=True,
    ).data

    assert response.data == serializer_data
