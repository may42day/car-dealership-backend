from rest_framework import status
import pytest


@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_customer", status.HTTP_400_BAD_REQUEST),
        ("specific_dealer", status.HTTP_403_FORBIDDEN),
        ("specific_supplier", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.enable_permissions
@pytest.mark.django_db
def test_customers_offers_create(api_client, request, user_with_role, response_status):
    """
    Checks API whether it's forbidden or not for different roles to creae customer offers.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/v1/orders/customers/offers")
    assert response.status_code == response_status


@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_dealer", status.HTTP_400_BAD_REQUEST),
        ("specific_customer", status.HTTP_403_FORBIDDEN),
        ("specific_supplier", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.enable_permissions
@pytest.mark.django_db
def test_dealers_offers_create(api_client, request, user_with_role, response_status):
    """
    Checks API whether it's forbidden or not for different roles to creae dealers offers.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/v1/orders/dealers/offers")
    assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_prefix", ["customers", "customers/total", "suppliers", "suppliers/total"]
)
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_dealer", status.HTTP_200_OK),
        ("specific_customer", status.HTTP_403_FORBIDDEN),
        ("specific_supplier", status.HTTP_403_FORBIDDEN),
        ("other_dealer", status.HTTP_403_FORBIDDEN),
    ],
)
def test_dealers_deals_with_customers(
    api_client, request, user_with_role, response_status, specific_dealer, url_prefix
):
    """
    Checks API whether it's allowed for specific dealers to check their delas history.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.get(
        f"/api/v1/orders/dealers/{specific_dealer.pk}/{url_prefix}"
    )
    assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize("url_prefix", ["dealers", "total/dealers"])
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_supplier", status.HTTP_200_OK),
        ("specific_dealer", status.HTTP_403_FORBIDDEN),
        ("specific_customer", status.HTTP_403_FORBIDDEN),
        ("other_dealer", status.HTTP_403_FORBIDDEN),
    ],
)
def test_suppliers_deals_list_allowed(
    api_client, request, user_with_role, response_status, specific_supplier, url_prefix
):
    """
    Checks API whether it's allowed only for suppliers to check their delas history.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.get(
        f"/api/v1/orders/suppliers/{specific_supplier.pk}/{url_prefix}"
    )
    assert response.status_code == response_status
