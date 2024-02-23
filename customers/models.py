from django.db import models
from django_countries.fields import CountryField

from common.models import BaseQuerySet
from cars.models import Car
from common.models import BaseModel
from users.models import UserProfile


class CustomerQuerySet(BaseQuerySet):
    """
    Customized query set manager for Customer model.
    Inherits from BaseQuerySet.
    """

    def total_deals(self):
        return self.prefetch_related("total_purchases")

    def customer(self, customer_id: int):
        return self.filter(id=customer_id)


class CustomerManager(models.Manager):
    """
    Customized manager for Customer model.
    """

    def active(self):
        return self.get_queryset().active()

    def pre_offer_queryset(self, customer_id: int):
        """
        Prepare queryset for handling customer offer
        """
        return self.get_queryset().active().customer(customer_id).total_deals()


class Customer(BaseModel):
    """
    Class to represent a customer entry
    Inherits from class BaselModel.

    Attributes
    ----------
    name : CharField
        name of customer
    balance : PositiveBigIntegerField
        customer balance
    place : CountryField
        customer location
    cars : ManyToManyField
        customer's cars
    user_profile : OneToOneField
        relation to user profile
    """

    name = models.CharField(max_length=255)
    balance = models.PositiveBigIntegerField(default=0)
    place = CountryField(blank=True, null=True)
    cars = models.ManyToManyField(Car)
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="customer_profile"
    )
    objects = CustomerManager.from_queryset(CustomerQuerySet)()

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of customer name
        """
        return f"{self.name}"
