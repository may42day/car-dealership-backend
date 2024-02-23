from rest_framework import status
import pytest


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_supplier", status.HTTP_200_OK),
        ("other_supplier", status.HTTP_403_FORBIDDEN),
    ],
)
def test_suppliers_update_allowed(
    api_client, specific_supplier, request, user_with_role, response_status
):
    """
    Checks API whether it's forbidden or not for supplier to update profile.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/api/v1/suppliers/{specific_supplier.pk}/")
    assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_supplier", status.HTTP_200_OK),
        ("other_supplier", status.HTTP_403_FORBIDDEN),
    ],
)
def test_suppliers_clinets_list(
    api_client, user_with_role, response_status, specific_supplier, request
):
    """
    Checks API whether it's forbidden or not for supplier to check clients.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/v1/suppliers/{specific_supplier.pk}/clients")
    assert response.status_code == response_status
