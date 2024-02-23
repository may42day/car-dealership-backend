import pytest
from rest_framework import status


@pytest.mark.django_db
def test_cars_endpoints_exists(api_client):
    """
    Checking whether specific routes exist in the cars app
    """
    url = "/api/auth/token"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/auth/token/refresh"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/auth/token/decode/"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
