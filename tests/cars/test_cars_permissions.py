from rest_framework import status
import pytest


@pytest.mark.enable_permissions
@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_with_role, response_status",
    [
        ("specific_customer", status.HTTP_403_FORBIDDEN),
        ("specific_dealer", status.HTTP_201_CREATED),
        ("specific_supplier", status.HTTP_201_CREATED),
    ],
)
def test_cars_creation(api_client, user_with_role, response_status, request):
    """
    Checks API whether it is forbidden or not to create car for user with different roles.
    """
    user = request.getfixturevalue(user_with_role).user_profile
    data = {
        "brand": "some_brand",
        "car_model": "some_car_model",
        "year_release": "2000",
    }
    api_client.force_authenticate(user=user)
    response = api_client.post("/api/v1/cars/", data=data, format="json")
    assert response.status_code == response_status
