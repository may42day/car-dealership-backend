import pytest
from rest_framework import status


@pytest.mark.django_db
def test_dealers_endpoints_exists(api_client, specific_dealer):
    """
    Checking whether specific routes exist in t he dealers app
    """
    url = "/api/v1/dealers/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/{specific_dealer.pk}"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/stock"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/stock/{specific_dealer.pk}"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/{specific_dealer.pk}/discounts"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/{specific_dealer.pk}/marketing-campaigns"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/{specific_dealer.pk}/suppliers"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/{specific_dealer.pk}/clients/deals"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/{specific_dealer.pk}/suppliers/deals"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/{specific_dealer.pk}/characteristics/add/"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/dealers/{specific_dealer.pk}/characteristics/remove/"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
