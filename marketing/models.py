from django.db import models

from cars.models import Car
from common.models import BaseModel
from dealers.models import Dealer
from suppliers.models import Supplier

import math

# WEIGHTS FOR estimate_foreceast_of_cooperation
WEIGHTS_PRICE_DIFFERENCE = {5: 0.2, 10: 0.4, 30: 0.8, 100: 1}
WEIGHTS_DISCOUNT_AMOUNT = {
    50: 0.3,
    100: 0.4,
    99999: 1,
}
WEIGHTS_DISCOUNT_COMPLETE_PERCENTAGE = {90: 1, 70: 0.8, 60: 0.5, 0: 0.1}
PASSING_WEIGHT = 0.5


class DiscountCounter(BaseModel):
    """
    An abstract class providing interface for price calculation.
    Inherits from class BaseModel.
    """

    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        abstract = True

    def count_price_with_discount(self, price: int) -> int:
        """
        Function for calculating price based on discount percentage.
        """
        if self.percentage == 0:
            return price
        else:
            return math.ceil(price * (100 - self.percentage) / 100)


class Discount(DiscountCounter, BaseModel):
    """
    A class to represent a discount for purchase.
    Inherits from class BaseModel.

    There are two types of discount:
    - Cumulative discount. Represent discount based on minimal quantity buyer must have for all time.
    - Bulk discount. Represent discount based on minimal quantity buyer must buy at once.

    Attributes
    ----------
    name : CharField
        name of discount
    min_amount : PositiveIntegerField
        minimal quantity the discount will act from
    percentage : DecimalField
        percenate of discount
    discount_type : CharField
        type of discount (store one of the choices)

    """

    DISCOUNT_TYPE_CHOICES = [("CD", "Cumulative discount"), ("BD", "Bulk discount")]
    name = models.CharField(max_length=255)
    min_amount = models.PositiveIntegerField()
    discount_type = models.CharField(
        max_length=2, choices=DISCOUNT_TYPE_CHOICES, default="CD"
    )

    class Meta:
        abstract = True

    def get_discount_percentage(
        self, total_purchases: int = 0, current_purchase_amount: int = 1
    ) -> float:
        """
        Function check if amount of purchases satisfies discounts conditions and returns discount percentage
        """
        if self.discount_type == "CD" and total_purchases >= self.min_amount:
            return self.percentage
        elif self.discount_type == "BD" and current_purchase_amount >= self.min_amount:
            return self.percentage
        return 0

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of discount name
        """
        return f"{self.name}"


class DealerDiscount(Discount):
    """
    A class to represent a dealer discounts.
    Inherits from class Discount.

    Attributes
    ----------
    dealer : ForeignKey
        relation to Dealer table
    """

    dealer = models.ForeignKey(
        Dealer, related_name="discounts", on_delete=models.CASCADE
    )


class SupplierDiscount(Discount):
    """
    A class to represent a supplier discounts.
    Inherits from class Discount.

    Attributes
    ----------
    dealer : ForeignKey
        relation to Dealer table
    """

    supplier = models.ForeignKey(
        Supplier, related_name="discounts", on_delete=models.CASCADE
    )

    def estimate_foreceast_of_cooperation(
        self, best_price, price_without_discount, total_purchases: int = 0
    ):
        """
        Funtion to estimate future cooperation with seller.

        Calculates weights based on set up weights for different parameters.
        It calculates meters and set a weight for it based on set up weights for every defined weight params.

        weight1_price - weight for percentage difference between best sellers price and forecast seller price.
        weight2_discount_amount - weight for total purchases amount(min amount in discount)
            which should be collected to complete discount.
        weight3_complete_percentage - weight for percentage of compliting total purchases
            based on current total dealer's purchases.
        """
        if self.discount_type != "CD":
            print("Unreachable. Use only for Cumulative Discount")
            return 0

        price_with_discount = self.count_price_with_discount(price_without_discount)
        if best_price < price_with_discount:
            return 0

        price_difference_percentage = 100 - (price_with_discount / best_price * 100)
        weight1_price = 0
        for key, value in WEIGHTS_PRICE_DIFFERENCE.items():
            if price_difference_percentage <= key:
                weight1_price = value
                break

        weight2_discount_amount = 0
        for key, value in WEIGHTS_DISCOUNT_AMOUNT.items():
            if self.min_amount <= key:
                weight2_discount_amount = value
                break

        dicount_complete_percentage = total_purchases / self.min_amount * 100
        weight3_complete_percentage = 0
        for key, value in WEIGHTS_DISCOUNT_COMPLETE_PERCENTAGE.items():
            if dicount_complete_percentage >= key:
                weight3_complete_percentage = value
                break

        total_weight = (
            weight1_price + weight2_discount_amount + weight3_complete_percentage
        ) / 3
        rounded_total_weight = round(total_weight, 1)
        return rounded_total_weight


class MarketingCampaign(DiscountCounter, BaseModel):
    """
    A abstract class to represent a marketing campaigns.
    Inherits from class BaseModel.

    Attributes
    ----------
    name : CharField
        name of campaign
    description : TextField
        description with event details
    percentage : DecimalField
        percenate of discount for every car
    cars : ManyToManyField
        cars which participate in event
    start_date : DateTimeField
        start date of campagin
    end_date : DateTimeField
        end date of campagin
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    cars = models.ManyToManyField(Car)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of campaign name
        """
        return f"{self.name}"


class DealerMarketingCampaign(MarketingCampaign):
    """
    A class to represent a dealer marketing campaigns.
    Inherits from class MarketingCampaign.

    Attributes
    ----------
    dealer : ForeignKey
        relation to Dealer table
    """

    dealer = models.ForeignKey(
        Dealer, related_name="marketing_campaigns", on_delete=models.CASCADE
    )


class SupplierMarketingCampaign(MarketingCampaign):
    """
    A class to represent a supplier marketing campaign entry.
    Inherits from class MarketingCampaign.

    Attributes
    ----------
    supplier : ForeignKey
        relation to Supplier table
    """

    supplier = models.ForeignKey(
        Supplier, related_name="marketing_campaigns", on_delete=models.CASCADE
    )
