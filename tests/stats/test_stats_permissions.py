from rest_framework import status
import pytest


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url, stats_owner, request_user, response_status",
    [
        (
            "/api/v1/stats/customers/",
            "specific_customer",
            "specific_customer",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "/api/v1/stats/customers/",
            "specific_customer",
            "other_customer",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "/api/v1/stats/dealers/",
            "specific_dealer",
            "specific_dealer",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "/api/v1/stats/dealers/",
            "specific_dealer",
            "other_dealer",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "/api/v1/stats/suppliers/",
            "specific_supplier",
            "specific_supplier",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "/api/v1/stats/suppliers/",
            "specific_supplier",
            "other_supplier",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_stats_get_permissions(
    api_client,
    request,
    url,
    stats_owner,
    request_user,
    response_status,
):
    """
    Checks API whether it's forbidden or not for checking specific stats.
    """
    stats_owner = request.getfixturevalue(stats_owner)
    request_user = request.getfixturevalue(request_user)

    api_client.force_authenticate(user=request_user.user_profile)
    response = api_client.get(f"{url}{stats_owner.pk}")
    assert response.status_code == response_status
