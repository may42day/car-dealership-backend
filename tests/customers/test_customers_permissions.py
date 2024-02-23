from rest_framework import status

import pytest


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_customer", status.HTTP_200_OK),
        ("other_customer", status.HTTP_403_FORBIDDEN),
    ],
)
def test_customers_update_allowed(
    api_client, specific_customer, user_with_role, response_status, request
):
    """
    Checks API whether it's forbidden or not for customer to update profile.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/api/v1/customers/{specific_customer.pk}/")
    assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_customer", status.HTTP_200_OK),
        ("other_customer", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.parametrize("url_prefix", ["cars", "purchase-history"])
def test_customers_list_orders(
    api_client, specific_customer, user_with_role, response_status, request, url_prefix
):
    """
    Checks API whether it's not forbidden for specific customer to check his orders history or his cars.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/v1/customers/{specific_customer.pk}/{url_prefix}")
    assert response.status_code == response_status
