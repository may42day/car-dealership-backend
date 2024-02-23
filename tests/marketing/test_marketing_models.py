import pytest
from ddf import G

from marketing.models import DealerDiscount, DealerMarketingCampaign


@pytest.mark.django_db
class TestDiscount:
    """
    Test class for discount model.
    """

    def test_bulk_discount_allowed(self):
        """
        Checking whether conditions for bulk discount are completed.
        """
        discount = G(DealerDiscount, min_amount=5, percentage=5, discount_type="BD")
        discount_percentage = discount.get_discount_percentage(
            current_purchase_amount=10
        )

        assert discount_percentage == 5

    def test_cumulative_discount_allowed(self):
        """
        Checking whether conditions for cumulative discount are completed.
        """
        discount = G(DealerDiscount, min_amount=5, percentage=5, discount_type="CD")
        discount_percentage = discount.get_discount_percentage(total_purchases=10)
        assert discount_percentage == 5

    def test_bulk_discount_not_allowed(self):
        """
        Checking whether conditions for bulk discount aren't completed.
        """
        discount = G(DealerDiscount, min_amount=5, percentage=5, discount_type="BD")
        discount_percentage = discount.get_discount_percentage(
            current_purchase_amount=2
        )

        assert discount_percentage == 0

    def test_cumulative_discount_not_allowed(self):
        """
        Checking whether conditions for cumulative discount aren't completed.
        """
        discount = G(DealerDiscount, min_amount=5, percentage=5, discount_type="CD")
        discount_percentage = discount.get_discount_percentage(total_purchases=2)
        assert discount_percentage == 0

    def test_discount_price_with_discount(self):
        """
        Checking correct price calculation with discount.
        """
        discount = G(DealerDiscount, min_amount=5, percentage=20, discount_type="CD")
        price_with_discount = discount.count_price_with_discount(price=100)
        assert price_with_discount == 80


@pytest.mark.django_db
def test_marketing_campaign_price_with_discount():
    """
    Checking correct price calculation with discount in marketing campaign.
    """
    marketing_campaign = G(DealerMarketingCampaign, percentage=5)
    price_with_discount = marketing_campaign.count_price_with_discount(price=100)
    assert price_with_discount == 95
