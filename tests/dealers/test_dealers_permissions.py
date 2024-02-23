from rest_framework import status
import pytest


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_dealer", status.HTTP_200_OK),
        ("other_dealer", status.HTTP_403_FORBIDDEN),
    ],
)
def test_dealers_update_allowed(
    api_client, specific_dealer, user_with_role, response_status, request
):
    """
    Checks API whether it's forbidden or not for dealer to update profile.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/api/v1/dealers/{specific_dealer.pk}/")
    assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_dealer", status.HTTP_200_OK),
        ("other_dealer", status.HTTP_403_FORBIDDEN),
    ],
)
def test_dealers_clinets_list(
    api_client, specific_dealer, user_with_role, response_status, request
):
    """
    Checks API whether it's forbidden or not for specific dealer to check his clients.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/v1/dealers/{specific_dealer.pk}/clients/deals")
    assert response.status_code == response_status
