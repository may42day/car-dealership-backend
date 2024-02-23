import pytest
from rest_framework import status


@pytest.mark.django_db
def test_customers_balance_showed(api_client, specific_customer):
    """
    Checking whether customer owner can see his balance.
    """
    api_client.force_authenticate(user=specific_customer.user_profile)

    url = f"/api/v1/customers/{specific_customer.pk}/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert "balance" in response.data


@pytest.mark.django_db
def test_customers_balance_hidden(api_client, other_customer, specific_customer):
    """
    Checking whether non-owner customer can't see other balance.
    """
    api_client.force_authenticate(user=other_customer.user_profile)

    url = f"/api/v1/customers/{specific_customer.pk}/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert "balance" not in response.data
