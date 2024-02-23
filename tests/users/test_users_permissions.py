from rest_framework import status
import pytest


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_prefix",
    [
        "sign-up",
        "sign-up/confirmation",
        "token/check",
        "reset-password",
        "reset-password/new",
        "1/change-email",
        "1/change-email/new",
        "1/change-login",
        "1/change-login/new",
    ],
)
def test_users_no_auth_allowed(api_client, url_prefix):
    """
    Checks user API router no auth required.
    """
    response = api_client.post(f"/api/v1/users/{url_prefix}")
    assert response.status_code != status.HTTP_401_UNAUTHORIZED


@pytest.mark.enable_permissions
@pytest.mark.django_db
class TestUserRouter:
    """
    Test class for checking users API router.
    Auth required.
    """

    @pytest.mark.parametrize("url_prefix", ["", "1/"])
    def test_users_get_user(self, api_client, url_prefix):
        """
        Checks user detail API auth required.
        """
        response = api_client.get(f"/api/v1/users/{url_prefix}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_user", status.HTTP_200_OK),
            ("other_user", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_users_update_user(
        self, api_client, specific_user, user_with_role, response_status, request
    ):
        """
        Checks update user API owner auth required.
        """
        user = request.getfixturevalue(user_with_role)
        api_client.force_authenticate(user=user)
        response = api_client.patch(f"/api/v1/users/{specific_user.pk}/")
        assert response.status_code == response_status

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_user", status.HTTP_204_NO_CONTENT),
            ("other_user", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_users_delete(
        self, api_client, specific_user, user_with_role, response_status, request
    ):
        """
        Checks delete user API auth owner required.
        """
        user = request.getfixturevalue(user_with_role)
        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/api/v1/users/{specific_user.pk}/")
        assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("admin_user", status.HTTP_200_OK),
        ("specific_user", status.HTTP_403_FORBIDDEN),
    ],
)
def test_users_block_user(
    api_client, specific_user, user_with_role, response_status, request
):
    """
    Checks block user API admin required.
    """
    user = request.getfixturevalue(user_with_role)
    api_client.force_authenticate(user=user)
    response = api_client.put(f"/api/v1/users/{specific_user.pk}/block")
    assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("admin_user", status.HTTP_200_OK),
        ("specific_user", status.HTTP_403_FORBIDDEN),
    ],
)
def test_users_unblock_user(
    api_client, specific_user, user_with_role, response_status, request
):
    """
    Checks unblock user API admin required.
    """
    user = request.getfixturevalue(user_with_role)
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"/api/v1/users/{specific_user.pk}/block")
    assert response.status_code == response_status
