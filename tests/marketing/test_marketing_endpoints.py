import pytest
from django_dynamic_fixture import G
from rest_framework import status

from cars.models import Car
from marketing.models import DealerMarketingCampaign, SupplierMarketingCampaign


@pytest.fixture
def car():
    """
    Fixture with car data
    """
    return G(Car)


@pytest.fixture
def dealer_campaign(specific_dealer):
    """
    Fixture with dealer campaign data
    """
    campaign = G(DealerMarketingCampaign, dealer=specific_dealer)
    return campaign


@pytest.fixture
def supplier_campaign(specific_supplier):
    """
    Fixture with supplier campaign data
    """
    campaign = G(SupplierMarketingCampaign, supplier=specific_supplier)
    return campaign


@pytest.mark.django_db
def test_dealers_update_campaign_car(api_client, specific_dealer, dealer_campaign, car):
    """
    Checks API to add or remove car from dealer's marketing campaign.
    """
    api_client.force_authenticate(user=specific_dealer.user_profile)

    data = {"car_id": car.pk}
    response = api_client.post(
        f"/api/v1/marketing/dealers/campaigns/{dealer_campaign.pk}/cars/add/",
        data=data,
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert car in dealer_campaign.cars.all()

    response = api_client.post(
        f"/api/v1/marketing/dealers/campaigns/{dealer_campaign.pk}/cars/remove/",
        data=data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert car not in dealer_campaign.cars.all()


@pytest.mark.django_db
def test_suppliers_update_campaign_car(
    api_client, specific_supplier, supplier_campaign, car
):
    """
    Checks API to add or remove car from dealer's marketing campaign.
    """
    api_client.force_authenticate(user=specific_supplier.user_profile)

    data = {"car_id": car.pk}
    response = api_client.post(
        f"/api/v1/marketing/suppliers/campaigns/{supplier_campaign.pk}/cars/add/",
        data=data,
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert car in supplier_campaign.cars.all()

    response = api_client.post(
        f"/api/v1/marketing/suppliers/campaigns/{supplier_campaign.pk}/cars/remove/",
        data=data,
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert car not in supplier_campaign.cars.all()
