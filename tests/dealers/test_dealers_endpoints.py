import pytest
from django_dynamic_fixture import G
from rest_framework import status

from cars.models import CarCharacteristic


@pytest.fixture
def car_characteristic():
    """
    Fixture with car charecteristic data
    """
    return G(CarCharacteristic)


@pytest.mark.django_db
def test_dealers_add_characteristics(api_client, specific_dealer, car_characteristic):
    """
    Checks API to add car characteristics to dealer profile.
    """
    data = {"car_characteristic_id": car_characteristic.pk}
    response = api_client.post(
        f"/api/v1/dealers/{specific_dealer.pk}/characteristics/add/",
        data=data,
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert car_characteristic in specific_dealer.car_characteristics.all()


@pytest.mark.django_db
def test_dealers_remove_characteristics(
    api_client, specific_dealer, car_characteristic
):
    """
    Checks API to remove car characteristics from dealer profile.
    """
    data = {"car_characteristic_id": car_characteristic.pk}
    response = api_client.post(
        f"/api/v1/dealers/{specific_dealer.pk}/characteristics/remove/",
        data=data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert car_characteristic not in specific_dealer.car_characteristics.all()


@pytest.mark.django_db
class TestDealerHiddenFields:
    def test_dealers_balance_showed(self, api_client, specific_dealer):
        """
        Checking whether supplier owner can see his balance.
        """
        api_client.force_authenticate(user=specific_dealer.user_profile)

        url = f"/api/v1/dealers/{specific_dealer.pk}/"
        response = api_client.get(url)
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert "balance" in response.data

    @pytest.mark.django_db
    def test_dealers_balance_hidden(self, api_client, other_dealer, specific_dealer):
        """
        Checking whether non-owner supplier can't see other balance.
        """
        api_client.force_authenticate(user=other_dealer.user_profile)

        url = f"/api/v1/dealers/{specific_dealer.pk}/"
        response = api_client.get(url)
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert "balance" not in response.data
