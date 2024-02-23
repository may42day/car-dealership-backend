import pytest
from rest_framework import status


@pytest.mark.django_db
class TestSupplierHiddenFields:
    def test_suppliers_balance_showed(self, api_client, specific_supplier):
        """
        Checking whether supplier owner can see his balance.
        """
        api_client.force_authenticate(user=specific_supplier.user_profile)

        url = f"/api/v1/suppliers/{specific_supplier.pk}/"
        response = api_client.get(url)
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert "balance" in response.data

    @pytest.mark.django_db
    def test_suppliers_balance_hidden(
        self, api_client, other_supplier, specific_supplier
    ):
        """
        Checking whether non-owner supplier can't see other balance.
        """
        api_client.force_authenticate(user=other_supplier.user_profile)

        url = f"/api/v1/suppliers/{specific_supplier.pk}/"
        response = api_client.get(url)
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert "balance" not in response.data
