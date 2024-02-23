from django.db import models
from django_countries.fields import CountryField
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.db.models import Sum, F

from cars.models import Car, CarCharacteristic
from common.models import AmountCalculator, BaseModel, BaseQuerySet
from dealers.models import Dealer
from suppliers.models import Supplier
from customers.models import Customer


class Offer(BaseModel):
    """
    An abstract class to represent a offer.
    Inherits from class BaseModel.

    Attributes
    ----------
    max_price : PositiveBigIntegerField
        the max price user ready to spend on car
    place : CountryField
        the location where user want to buy a car
    is_closed : BooleanField
        shows if the deal is closed/completed
    bought_car : ForeignKey
        car bough during the deal
    car_price : PositiveBigIntegerField
        price per 1 car
    """

    max_price = models.PositiveBigIntegerField()
    place = CountryField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    bought_car = models.ForeignKey(Car, on_delete=models.PROTECT, blank=True, null=True)
    car_price = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of offer id
        """
        return f"Offer #{self.pk}"


class DealerOfferQuerySet(BaseQuerySet):
    def orders_history(self):
        return self.prefetch_related("orders_history")

    def dealer(self, dealer_id: int):
        return self.filter(dealer__id=dealer_id).select_related("dealer")

    def dealer_history(self):
        return self.prefetch_related("dealer__orders_history")

    def car(self):
        return self.select_related("car")


class DealerOfferManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return DealerOfferQuerySet(self.model, using=self._db)

    def prepare_offer(self, dealer_id: int):
        """
        Creates queryset with all necessary data for handling dealer offer.
        """
        return self.get_queryset().dealer(dealer_id).car().dealer_history()


class DealerOffer(Offer):
    """
    A class to represent a dealer offer entry.
    Dealer points the price and car to make a deal.
    Inherits from class Offer.

    Attributes
    ----------
    dealer : ForeignKey
        customer created the offer
    car : ForeignKey
        the car user wants to buy
    amount : PositiveIntegerField
        amount of cars dealer want to buy

    """

    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT)
    car = models.ForeignKey(
        Car, related_name="dealers_offers", on_delete=models.PROTECT
    )
    amount = models.PositiveIntegerField()

    objects = DealerOfferManager.from_queryset(DealerOfferQuerySet)()

    def is_valid_for_offer(self) -> bool:
        """
        Function to check whether offer info is enough for creating offer
        Generally it checks car or all characteristics fields to be specified
        Only car or car characteristics must be specified one time at once
        """
        if (self.characteristic and self.car) or (
            not self.characteristic and not self.car
        ):
            return False
        elif self.characteristic and (
            not self.characteristic.brand
            or not self.characteristic.car_model
            or not self.characteristic.generation
        ):
            return False
        else:
            return True


class CustomerOfferQuerySet(BaseQuerySet):
    def customer(self, customer_id: int):
        return self.filter(customer__id=customer_id).select_related("customer")

    def car(self):
        return self.select_related("car")

    def characteristic(self):
        return self.select_related("characteristic")

    def customer_total_purchases(self):
        return self.prefetch_related("customer__total_purchases")


class CustomerOfferManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return CustomerOfferQuerySet(self.model, using=self._db)

    def prepare_offer(self, customer_id: int):
        """
        Creates queryset with all necessary data for handling customer offer.
        """
        return (
            self.get_queryset()
            .car()
            .characteristic()
            .customer_total_purchases()
            .customer(customer_id)
        )


class CustomerOffer(Offer):
    """
    A class to represent a customer offer entry.
    Customer points the price and car/car characteristics to make a deal.
    Must be set only one of car/car characteristics at once.
    Inherits from class Offer.

    Attributes
    ----------
    customer : ForeignKey
        customer created the offer
    car : ForeignKey
        the car user wants to buy
    characteristic : ForeignKey
        the characheristic of car user want to buy
    """

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    car = models.ForeignKey(
        Car,
        on_delete=models.PROTECT,
        related_name="customers_offers",
        blank=True,
        null=True,
    )
    characteristic = models.ForeignKey(
        CarCharacteristic, on_delete=models.PROTECT, blank=True, null=True
    )

    objects = CustomerOfferManager.from_queryset(CustomerOfferQuerySet)()

    def is_valid_for_offer(self) -> bool:
        """
        Function to check whether offer info is enough for creating offer
        Generally it checks car or all characteristics fields to be specified
        Only car or car characteristics must be specified one time at once
        """
        if (self.characteristic and self.car) or (
            not self.characteristic and not self.car
        ):
            return False
        elif self.characteristic and (
            not self.characteristic.brand
            or not self.characteristic.car_model
            or not self.characteristic.generation
        ):
            return False
        else:
            return True


class DealHistory(BaseModel):
    """
    An abstract class to represent a deal history between two participants
    Inherits from class BaseModel.

    Attributes
    ----------
    car : ForeignKey
        car on sale
    amount : PositiveIntegerField
        amount of selling cars
    price_per_one : BigIntegerField
        price per 1 car qty
    date : DateTimeField
        date of the deal
    """

    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(default=1)
    price_per_one = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of amount of cars model and its amount in deal
        """
        return f"{self.car.car_model} ({self.amount})"


class CommonDealsQuerySet(models.QuerySet):
    """
    Common models for deals queryset managers.
    """

    def count_unique(self):
        """
        Deletes duplicates and count total amount of entries.
        """
        return self.distinct().count()

    def total_sum(self):
        return self.aggregate(total_sum=Sum(F("amount") * F("price_per_one")))


class CustomerDealsManager(models.Manager):
    """
    A queryset manager for customer's deals with dealers.
    """

    def get_total_amount_of_cars(self, filter_params: dict) -> QuerySet:
        """
        Calculates total amount of cars in deals for specific or full period based on filter params.
        """
        return self.filter(**filter_params).aggregate(total_amount=Sum(F("amount")))[
            "total_amount"
        ]

    def get_total_cost(self, filter_params: dict) -> QuerySet:
        """
        Calculates total cost of cars for specific or full period based on filter params.
        """
        return self.filter(**filter_params).total_sum()["total_sum"]

    def get_amount_of_unique_clients(self, filter_params: dict) -> QuerySet:
        """
        Calculates unique clients in deals for specific or full period based on filter params.
        """
        return self.filter(**filter_params).values("customer").count_unique()

    def get_amount_of_sold_unique_cars(self, filter_params: dict) -> QuerySet:
        """
        Calculates unique cars in deals for specific or full period based on filter params.
        """
        return self.filter(**filter_params).values("car").count_unique()


class CustomerDealsHistory(DealHistory):
    """
    A class to represent a deal between customer and dealer.
    Inherits from class DealHistory.

    Attributes
    ----------
    customer : ForeignKey
        relation to Customer table
    dealer : ForeignKey
        relation to Dealer table
    """

    customer = models.ForeignKey(
        Customer, related_name="history", on_delete=models.CASCADE
    )
    dealer = models.ForeignKey(
        Dealer, related_name="customer_history", on_delete=models.CASCADE
    )

    objects = CustomerDealsManager.from_queryset(CommonDealsQuerySet)()


class DealerDealsManager(models.Manager):
    """
    A queryset manager for dealers's deals with suppliers.
    """

    def get_total_amount_of_cars(self, filter_params: dict) -> QuerySet:
        """
        Calculates total amount of cars in deals for specific or full period based on filter params.
        """
        return self.filter(**filter_params).aggregate(total_amount=Sum(F("amount")))[
            "total_amount"
        ]

    def get_total_cost(self, filter_params: dict) -> QuerySet:
        """
        Calculates total cost of cars for specific or full period based on filter params.
        """
        return self.filter(**filter_params).total_sum()["total_sum"]

    def get_amount_of_unique_clients(self, filter_params: dict) -> QuerySet:
        """
        Calculates unique clients in deals for specific or full period based on filter params.
        """
        return self.filter(**filter_params).values("dealer").count_unique()

    def get_amount_of_sold_unique_cars(self, filter_params: dict) -> QuerySet:
        """
        Calculates unique cars in deals for specific or full period based on filter params.
        """
        return self.filter(**filter_params).values("car").count_unique()


class DealerDealsHistory(DealHistory):
    """
    A class to represent a deal between dealer and supplier
    Inherits from class DealHistory.

    Attributes
    ----------
    dealer : ForeignKey
        relation to Dealer table
    supplier : ForeignKey
        relation to Supplier table
    """

    dealer = models.ForeignKey(Dealer, related_name="history", on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, related_name="dealer_history", on_delete=models.CASCADE
    )

    objects = DealerDealsManager.from_queryset(CommonDealsQuerySet)()


class TotalDealerPurchase(AmountCalculator, BaseModel):
    """
    A class to represent a total amount of car sold from dealer to customer.
    Inherits from class BaseModel.

    Attributes
    ----------
    customer : ForeignKey
        relation to Customer table
    dealer : ForeignKey
        relation to Dealer table
    amount : PositiveBigIntegerField
        total amount of cars sold to customer
    """

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="total_purchases"
    )
    dealer = models.ForeignKey(
        Dealer, related_name="total_purchases", on_delete=models.CASCADE
    )
    amount = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of customer name his total purchases
        """
        return f"{self.customer.name} ({self.amount})"


class TotalSupplierPurchase(AmountCalculator, BaseModel):
    """
    A class to represent a total amount of car sold from supplier to dealer.
    Inherits from class BaseModel.

    Attributes
    ----------
    dealer : ForeignKey
        relation to Dealer table
    supplier : ForeignKey
        relation to Supplier table
    amount : PositiveBigIntegerField
        total amount of cars sold to dealer
    """

    dealer = models.ForeignKey(
        Dealer, related_name="orders_history", on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, related_name="total_purchases", on_delete=models.CASCADE
    )
    amount = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of dealer name his total purchases
        """
        return f"{self.dealer.name} ({self.amount})"
