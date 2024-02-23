import pytest
from rest_framework import status


@pytest.mark.django_db
def test_customers_endpoints_exists(api_client, specific_customer):
    """
    Checking whether specific routes exist in the customers app
    """
    api_client.force_authenticate(user=specific_customer.user_profile)

    url = "/api/v1/customers/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/customers/{specific_customer.pk}"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/customers/{specific_customer.pk}/cars"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/customers/{specific_customer.pk}/purchase-history"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
