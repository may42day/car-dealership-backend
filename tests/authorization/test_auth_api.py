import jwt

import pytest
from ddf import G
from rest_framework import status
from car_dealership.settings import SECRET_KEY

from users.models import UserProfile


@pytest.fixture
def activated_user() -> UserProfile:
    user = G(
        UserProfile,
        role=UserProfile.CUSTOMER,
        username="some_username",
        is_active=True,
    )
    user.set_password("some_password")
    user.save()
    return user


@pytest.fixture
def auth_url() -> str:
    return "/api/auth/token/"


@pytest.mark.django_db
class TestAuthAPI:
    """
    Test class for auth API with JWT logic.
    """

    def test_auth_get_token(self, api_client, activated_user, auth_url):
        """
        Gets token and checks JWT payload.
        """
        data = {"username": activated_user.username, "password": "some_password"}
        response = api_client.post(auth_url, data=data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"]
        assert response.data["refresh"]

        payload = jwt.decode(response.data["access"], SECRET_KEY, algorithms=["HS256"])

        assert payload["user_id"] == activated_user.pk
        assert payload["role"] == activated_user.role
        assert payload["is_staff"] is False

    def test_auth_refresh_token(self, api_client, activated_user, auth_url):
        """
        Gets refresh token and gets new token
        """

        data = {"username": activated_user.username, "password": "some_password"}
        response = api_client.post(auth_url, data=data, format="json")

        refresh_token = response.data["refresh"]
        url = f"{auth_url}refresh/"
        response = api_client.post(url, data={"refresh": refresh_token}, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"]
