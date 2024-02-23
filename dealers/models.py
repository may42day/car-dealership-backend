from datetime import datetime, timedelta

from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, Prefetch, Sum

from cars.models import CarCharacteristic, CarStockItem
from common.models import BaseQuerySet, Company
from suppliers.models import Supplier
from customers.models import Customer


class DealerQuerySet(BaseQuerySet):
    def orders_history(self):
        return self.prefetch_related("orders_history")

    def dealer(self, dealer_id: int):
        return self.filter(id=dealer_id)

    def stock(self):
        return self.prefetch_related("stock__car")

    def car_characteristics(self):
        return self.prefetch_related("car_characteristics")

    def discounts(self):
        return self.prefetch_related("discounts")

    def marketing_campaigns(self):
        return self.prefetch_related("marketing_campaigns__cars")

    def three_month_history(self):
        """
        Takes deals history for last 3 months and preload total amount of purchases for all suppliers.
        """
        from orders.models import CustomerDealsHistory

        three_month_ago = datetime.now() - timedelta(days=90)
        customer_history_filter = Q(date__gte=three_month_ago)
        customer_history_prefetch = Prefetch(
            "customer_history",
            queryset=CustomerDealsHistory.objects.filter(customer_history_filter)
            .annotate(total_amount=Sum("amount"))
            .select_related("car"),
            to_attr="three_month_history",
        )

        return self.prefetch_related(customer_history_prefetch)


class DealerManager(models.Manager):
    """
    Customized manager for Dealer model.
    """

    def get_queryset(self) -> QuerySet:
        return DealerQuerySet(self.model, using=self._db)

    def pre_order_queryset(self, dealer_id: int):
        """
        Creates queryset with all necessary data for completing regular order purchase.
        """
        return (
            self.get_queryset()
            .active()
            .orders_history()
            .three_month_history()
            .dealer(dealer_id)
        )

    def prepare_for_offer(self):
        """
        Creates queryset with all necessary data for completing customer's offer.
        """
        return (
            self.get_queryset()
            .active()
            .stock()
            .marketing_campaigns()
            .car_characteristics()
            .discounts()
        )

    def active(self):
        return self.get_queryset().active()

    def pre_customer_order_queryset(self):
        """
        Creates queryset with all necessary data for completing customer offer.
        """
        return self.get_queryset().active().stock().marketing_campaigns().discounts()


class Dealer(Company):
    """
    A class to represent a dealer entry
    Inherits from class Company.

    Attributes
    ----------
    customers : ManyToManyField
        relation to Customer table
    suppliers : ManyToManyField
        relation to Supplier table
    car_characteristics : ManyToManyField
        relation to CarCharacteristic table
    """

    customers = models.ManyToManyField(Customer)
    suppliers = models.ManyToManyField(Supplier)
    car_characteristics = models.ManyToManyField(CarCharacteristic)

    objects = DealerManager.from_queryset(DealerQuerySet)()


class DealerStockItem(CarStockItem):
    """
    A class to represent a stock of cars for dealer.
    Related to :model:'dealers.Dealer'
    Inherits from class CarStockItem.

    Attributes
    ----------
    dealer : ForeignKey
        relation to Dealer table
    """

    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="stock")
