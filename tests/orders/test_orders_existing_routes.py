import pytest
from rest_framework import status


@pytest.mark.django_db
def test_orders_endpoints_exists(api_client):
    """
    Checking whether specific routes exist in the orders app
    """
    url = "/api/v1/orders/customers/offers"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/orders/dealers/offers"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/orders/customers/1"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/orders/dealers/1/customers"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/orders/dealers/1/customers/total"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/orders/dealers/1/suppliers"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/orders/dealers/1/suppliers/total"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/orders/suppliers/1/dealers"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/orders/suppliers/1/total/dealers"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
