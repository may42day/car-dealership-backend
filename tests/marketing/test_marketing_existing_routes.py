import pytest
from rest_framework import status


@pytest.mark.django_db
def test_marketing_endpoints_exists(api_client):
    """
    Checking whether specific routes exist in the marketing app
    """
    url = "/api/v1/marketing/dealers/campaigns"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/marketing/dealers/campaigns/1/cars/add/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/marketing/dealers/campaigns/1/cars/remove/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/marketing/suppliers/campaigns"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/marketing/suppliers/campaigns/1/cars/add/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/marketing/suppliers/campaigns/1/cars/remove/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/marketing/dealers/discounts"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/marketing/suppliers/discounts"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
