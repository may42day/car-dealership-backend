from rest_framework import status
import pytest


@pytest.mark.enable_permissions
@pytest.mark.django_db
class TestDealerMarketingAPI:
    """
    Test class for checking dealer's marketing campaign API.
    """

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_dealer", status.HTTP_400_BAD_REQUEST),
            ("specific_supplier", status.HTTP_403_FORBIDDEN),
            ("specific_customer", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_dealers_campaign_create_allowed(
        self, api_client, user_with_role, response_status, request
    ):
        """
        Checks API whether it's forbidden or not for different roles to create campaign.
        """
        user = request.getfixturevalue(user_with_role).user_profile
        api_client.force_authenticate(user=user)
        response = api_client.post(f"/api/v1/marketing/dealers/campaigns/")
        assert response.status_code == response_status

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_dealer", status.HTTP_200_OK),
            ("other_dealer", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_dealers_campaign_update_allowed(
        self, api_client, specific_dealer, user_with_role, response_status, request
    ):
        """
        Checks API whether it's forbidden or not for dealer to update campaign.
        """
        user = request.getfixturevalue(user_with_role).user_profile
        api_client.force_authenticate(user=user)
        response = api_client.patch(
            f"/api/v1/marketing/dealers/campaigns/{specific_dealer.marketing_campaigns.first().pk}/"
        )
        assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
class TestDealerDiscountAPI:
    """
    Test class for checking dealer's discount API.
    """

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_dealer", status.HTTP_400_BAD_REQUEST),
            ("specific_supplier", status.HTTP_403_FORBIDDEN),
            ("specific_customer", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_dealers_discounts_create(
        self, api_client, user_with_role, response_status, request
    ):
        """
        Checks API whether it's forbidden or not for different roles to create discount.
        """
        user = request.getfixturevalue(user_with_role).user_profile
        api_client.force_authenticate(user=user)
        response = api_client.post(f"/api/v1/marketing/dealers/discounts/")
        assert response.status_code == response_status

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_dealer", status.HTTP_200_OK),
            ("other_dealer", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_dealers_discounts_update(
        self, api_client, specific_dealer, user_with_role, response_status, request
    ):
        """
        Checks API whether it's forbidden or not for dealer to update discount.
        """
        user = request.getfixturevalue(user_with_role).user_profile
        api_client.force_authenticate(user=user)
        response = api_client.patch(
            f"/api/v1/marketing/dealers/discounts/{specific_dealer.discounts.first().pk}/"
        )
        assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
class TestSupplierMarketingAPI:
    """
    Test class for checking cars API.
    """

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_supplier", status.HTTP_400_BAD_REQUEST),
            ("specific_dealer", status.HTTP_403_FORBIDDEN),
            ("specific_customer", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_suppliers_campaign_create_allowed(
        self, api_client, user_with_role, response_status, request
    ):
        """
        Checks API whether it's forbidden or not for different roles to create campaign.
        """
        user = request.getfixturevalue(user_with_role).user_profile
        api_client.force_authenticate(user=user)
        response = api_client.post(f"/api/v1/marketing/suppliers/campaigns/")
        assert response.status_code == response_status

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_supplier", status.HTTP_200_OK),
            ("other_supplier", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_suppliers_campaign_update_allowed(
        self, api_client, specific_supplier, user_with_role, response_status, request
    ):
        """
        Checks API whether it's forbidden or not for supplier to update campaign.
        """
        user = request.getfixturevalue(user_with_role).user_profile
        api_client.force_authenticate(user=user)
        response = api_client.patch(
            f"/api/v1/marketing/suppliers/campaigns/{specific_supplier.marketing_campaigns.first().pk}/"
        )
        assert response.status_code == response_status


@pytest.mark.enable_permissions
@pytest.mark.django_db
class TestSupplierDiscountAPI:
    """
    Test class for checking cars API.
    """

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_supplier", status.HTTP_400_BAD_REQUEST),
            ("specific_dealer", status.HTTP_403_FORBIDDEN),
            ("specific_customer", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_dealers_discounts_create(
        self, api_client, user_with_role, response_status, request
    ):
        """
        Checks API whether it's forbidden or not for different roles to create discount.
        """
        user = request.getfixturevalue(user_with_role).user_profile
        api_client.force_authenticate(user=user)
        response = api_client.post(f"/api/v1/marketing/suppliers/discounts/")
        assert response.status_code == response_status

    @pytest.mark.parametrize(
        "user_with_role, response_status",
        [
            ("specific_supplier", status.HTTP_200_OK),
            ("other_supplier", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_dealers_discounts_update(
        self, api_client, specific_supplier, user_with_role, response_status, request
    ):
        """
        Checks API whether it's forbidden or not for supplier to update discount.
        """
        user = request.getfixturevalue(user_with_role).user_profile
        api_client.force_authenticate(user=user)
        response = api_client.patch(
            f"/api/v1/marketing/suppliers/discounts/{specific_supplier.discounts.first().pk}/"
        )
        assert response.status_code == response_status
