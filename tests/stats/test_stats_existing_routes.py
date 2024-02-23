import pytest
from rest_framework import status


@pytest.mark.django_db
def test_stats_endpoints_exists(
    api_client, specific_customer, specific_dealer, specific_supplier
):
    """
    Checking whether specific routes exist in the stats app
    """
    url = f"/api/v1/stats/customers/{specific_customer.pk}"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/stats/dealers/{specific_dealer.pk}"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/stats/suppliers/{specific_supplier.pk}"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND
