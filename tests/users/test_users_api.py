import pytest
from ddf import G
import json
from rest_framework import status

from customers.models import Customer
from dealers.models import Dealer
from suppliers.models import Supplier
from users.models import ConfirmationToken, UserProfile


@pytest.fixture
def sign_up_data() -> dict:
    return {
        "username": "some_username",
        "password": "some_password",
        "first_name": "some_first_name",
        "last_name": "some_last_name",
        "email": "email@email.com",
    }


@pytest.fixture
def sign_up_url() -> str:
    return "/api/v1/users/sign-up"


@pytest.mark.enable_signals
@pytest.mark.django_db
class TestSignUp:
    """
    Class test for checking users registration with different roles.
    """

    def test_users_sign_up_customer(self, api_client, sign_up_data, sign_up_url):
        """
        Test for checking user-customer registration.
        """
        sign_up_data["role"] = "customer"
        response = api_client.post(sign_up_url, data=sign_up_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        user = UserProfile.objects.get(username="some_username")
        assert user
        customer = Customer.objects.get(user_profile=user.pk)
        assert customer

    @pytest.mark.django_db
    def test_users_sign_up_dealer(self, api_client, sign_up_data, sign_up_url):
        """
        Test for checking user-dealer registration.
        """
        sign_up_data["role"] = "dealer"
        response = api_client.post(sign_up_url, data=sign_up_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        user = UserProfile.objects.get(username="some_username")
        assert user
        dealer = Dealer.objects.get(user_profile=user.pk)
        assert dealer

    @pytest.mark.django_db
    def test_users_sign_up_supplier(self, api_client, sign_up_data, sign_up_url):
        """
        Test for checking user-supplier registration.
        """
        sign_up_data["role"] = "supplier"
        response = api_client.post(sign_up_url, data=sign_up_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        user = UserProfile.objects.get(username="some_username")
        assert user
        supplier = Supplier.objects.get(user_profile=user.pk)
        assert supplier


@pytest.mark.django_db
class TestBlockUser:
    """
    Test API for block/unblock user.
    """

    def test_users_block(self, api_client, specific_user):
        """
        Test for checking API to block user.
        """

        url = f"/api/v1/users/{specific_user.pk}/block"
        response = api_client.put(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        user = UserProfile.objects.get(pk=specific_user.pk)
        assert user.is_active is False

    def test_users_unblock(self, specific_user, api_client):
        """
        Test for checking API to unblock user.
        """

        url = f"/api/v1/users/{specific_user.pk}/block"

        response = api_client.delete(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        user = UserProfile.objects.get(pk=specific_user.pk)
        assert user.is_active is True


@pytest.fixture
def users_router_url() -> str:
    return "/api/v1/users/"


@pytest.mark.django_db
class TestUsersRouter:
    """
    Test main users API
    """

    def test_users_get_users(self, api_client, users_router_url):
        """
        Test for checking API router to get all users
        """
        user1 = G(UserProfile)
        user2 = G(UserProfile)

        response = api_client.get(users_router_url)

        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert any(user["pk"] == user1.pk for user in data)
        assert any(user["pk"] == user2.pk for user in data)

    def test_users_get_user(self, api_client, users_router_url):
        """
        Test for checking API router to get specific user.
        """
        user = G(UserProfile)

        url = f"{users_router_url}{user.pk}/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert data["pk"] == user.pk

    def test_users_update_user(self, api_client, users_router_url):
        """
        Test for checking API router to update user data.
        """
        user = G(UserProfile, first_name="Charlie", last_name="Williams")
        data = {
            "first_name": "Thomas",
            "last_name": "Roy",
        }

        url = f"{users_router_url}{user.pk}/"
        response = api_client.patch(url, data=data, format="json")

        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert data["first_name"] == "Thomas"
        assert data["last_name"] == "Roy"

    def test_users_change_password(self, api_client, users_router_url):
        """
        Test for checking API router to change user's password.
        """
        user = G(UserProfile)
        user.set_password("some_password")
        user.save()
        data = {
            "old_password": "some_password",
            "new_password": "some_new_password",
        }

        url = f"{users_router_url}{user.pk}/change-password/"
        response = api_client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_200_OK
        user = UserProfile.objects.get(pk=user.pk)
        assert user.check_password("some_new_password")


@pytest.mark.django_db
def test_users_change_login(api_client):
    """
    Test for checking API to change user's login.
    """
    user = G(UserProfile, username="login999")
    token = G(ConfirmationToken, token_type=ConfirmationToken.LOGIN_CHANGE)
    data = {
        "new_username": "login111",
        "token": token.token,
        "token_type": token.token_type,
    }

    url = f"/api/v1/users/{user.pk}/change-login/new"
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user = UserProfile.objects.get(username="login111")
    assert user


@pytest.mark.django_db
def test_users_change_email(api_client):
    """
    Test for checking API to change user's email.
    """
    user = G(UserProfile, email="qqbb@mail.com")
    token = G(ConfirmationToken, token_type=ConfirmationToken.EMAIL_CHANGE)
    data = {
        "new_email": "yyuu@mail.com",
        "token": token.token,
        "token_type": token.token_type,
    }

    url = f"/api/v1/users/{user.pk}/change-email/new"
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user = UserProfile.objects.get(email="yyuu@mail.com")
    assert user


@pytest.mark.django_db
def test_users_reset_password(api_client):
    """
    Test for checking API to reset user's password.
    """
    user = G(UserProfile)
    token = G(ConfirmationToken, token_type=ConfirmationToken.PASSW_RESET, user=user)
    data = {
        "new_password": "new_password",
        "token": token.token,
        "token_type": token.token_type,
    }

    url = f"/api/v1/users/reset-password/new"
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user = UserProfile.objects.get(pk=user.pk)
    assert user.check_password("new_password")


@pytest.mark.django_db
def test_users_confirm_registration(api_client):
    """
    Test for checking API to confirm user's registration.
    """
    user = G(UserProfile, is_active=False)
    token = G(ConfirmationToken, token_type=ConfirmationToken.REG_CONFIRM, user=user)

    url = f"/api/v1/users/sign-up/confirmation?token={token.token}&token_type=reg"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    user = UserProfile.objects.get(pk=user.pk)
    assert user.is_active


@pytest.mark.django_db
def test_users_check_token(api_client):
    """
    Test for checking API to check whether token is valid and not expired.
    """
    token = G(ConfirmationToken, token_type=ConfirmationToken.LOGIN_CHANGE)

    url = f"/api/v1/users/token/check?token={token.token}&token_type=log"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserHiddenFields:
    def test_users_is_active_showed(self, api_client, specific_user):
        """
        Checking whether user owner can see his email.
        """
        api_client.force_authenticate(user=specific_user)

        url = f"/api/v1/users/{specific_user.pk}/"
        response = api_client.get(url)
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert "is_active" in response.data

    @pytest.mark.django_db
    def test_users_is_active_hidden(self, api_client, other_user, specific_user):
        """
        Checking whether non-owner user can't see other email.
        """
        api_client.force_authenticate(user=other_user)

        url = f"/api/v1/users/{specific_user.pk}/"
        response = api_client.get(url)
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert "is_active" not in response.data
