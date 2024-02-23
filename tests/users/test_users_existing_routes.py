import pytest
from ddf import G
from rest_framework import status


@pytest.mark.django_db
def test_users_endpoints_exists(api_client, specific_user):
    """
    Checking whether specific routes exist in the users app.
    """

    url = "/api/v1/users/sign-up"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/users/sign-up/confirmation"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = "/api/v1/users/"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/{specific_user.pk}"
    response = api_client.get(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/{specific_user.pk}/change-email"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/{specific_user.pk}/change-email/new"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/{specific_user.pk}/change-password"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/{specific_user.pk}/change-login"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/{specific_user.pk}/change-login/new"
    response = api_client.post(url)
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/{specific_user.pk}/block"
    response = api_client.put(url, format="json")
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/{specific_user.pk}/block"
    response = api_client.delete(url, format="json")
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/token/check"
    response = api_client.delete(url, format="json")
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/token/check"
    response = api_client.delete(url, format="json")
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/reset-password"
    response = api_client.delete(url, format="json")
    assert response.status_code != status.HTTP_404_NOT_FOUND

    url = f"/api/v1/users/reset-password/new"
    response = api_client.delete(url, format="json")
    assert response.status_code != status.HTTP_404_NOT_FOUND
