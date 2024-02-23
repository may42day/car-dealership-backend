import pytest
from rest_framework import status


@pytest.mark.django_db
def test_suppliers_endpoints_exists(api_client):
    """
    Checking whether specific routes exist in the suppliers app
    """
    url = "/api/v1/suppliers/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/suppliers/1"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/suppliers/stock/1"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/suppliers/1/discounts"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/suppliers/1/marketing-campaigns"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/suppliers/1/clients"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
