import pytest
from rest_framework import status


@pytest.mark.django_db
def test_cars_endpoints_exists(api_client):
    """
    Checking whether specific routes exist in the cars app
    """
    url = "/api/v1/cars/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/cars/1"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/cars/characteristics/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/cars/characteristics/1"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/cars/characteristics/1/pick-up-cars"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
