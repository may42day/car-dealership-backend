from django.db import models
from django.db.models.query import QuerySet

from cars.models import Car, CarStockItem
from common.models import BaseQuerySet, Company


class SupplierQuerySet(BaseQuerySet):
    def stock(self):
        return self.prefetch_related("stock__car")

    def marketing_campaigns(self):
        return self.prefetch_related("marketing_campaigns__cars")

    def discounts(self):
        return self.prefetch_related("discounts")


class SupplierManager(models.Manager):
    """
    Customized manager for Supplier model.
    """

    def get_queryset(self) -> QuerySet:
        return SupplierQuerySet(self.model, using=self._db)

    def pre_order_queryset(self):
        """
        Creates queryset with all necessary data for completing order.
        """
        return self.get_queryset().active().stock().marketing_campaigns().discounts()


class Supplier(Company):
    """
    Class to represent a supplier entry
    Inherits from class Company.

    Attributes
    ----------
    cars : ManyToManyField
        cars on sale
    """

    cars = models.ManyToManyField(Car)

    objects = SupplierManager()


class SupplierStockItem(CarStockItem):
    """
    A class to represent a stock of cars for supplier.
    Related to :model:'suppliers.Supplier'.
    Inherits from class CarStockItem.

    Attributes
    ----------
    supplier : ForeignKey
        relation to Supplier table

    """

    supplier = models.ForeignKey(
        Supplier, related_name="stock", on_delete=models.CASCADE
    )
