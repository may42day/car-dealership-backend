from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from customers.models import Customer

from orders.models import (
    CustomerOffer,
    CustomerDealsHistory,
    DealerDealsHistory,
    DealerOffer,
    TotalDealerPurchase,
    TotalSupplierPurchase,
)


class CustomerOfferSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for CustomerOffer model.

    Allows conversion of CustomerOffer objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - customer (ForeignKey, read-only) - customer created the offer.
        - characteristic (ForeignKey) - the characheristic of car user want to buy.
        - car (ForeignKey) - the car user wants to buy.
        - max_price (PositiveBigIntegerField) - the max price user ready to spend on car.
        - place (CountryField) - the location where user want to buy a car.
        - is_closed (BooleanField, read-only) - shows if the deal is closed/completed.
        - bought_car (ForeignKey, read-only) - car bought during the deal.
        - car_price (PositiveBigIntegerField, read-only) - price per 1 car.
    """

    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), required=False
    )

    class Meta:
        model = CustomerOffer
        fields = [
            "pk",
            "customer",
            "characteristic",
            "car",
            "max_price",
            "place",
            "is_closed",
            "bought_car",
            "car_price",
        ]
        read_only_fields = ["is_closed", "bought_car", "car_price"]


class DealerOfferSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for DealerOffer model.

    Allows conversion of DealerOffer objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - dealer (ForeignKey, read-only) - dealer created the offer.
        - car (ForeignKey) - the car user wants to buy.
        - amount (PositiveIntegerField) - amount of cars dealer want to buy.
        - max_price (PositiveBigIntegerField) - the max price dealer ready to spend for one car.
        - place (CountryField) - the location where dealer wants to buy a car.
        - is_closed (BooleanField, read-only) - shows if the deal is closed/completed.
        - bought_car (ForeignKey, read-only) - car bought during the deal.
        - car_price (PositiveBigIntegerField, read-only) - price per 1 car.
    """

    class Meta:
        model = DealerOffer
        fields = [
            "pk",
            "dealer",
            "car",
            "amount",
            "max_price",
            "place",
            "is_closed",
            "bought_car",
            "car_price",
        ]
        read_only_fields = ["dealer", "is_closed", "bought_car", "car_price"]


class CustomerDealsHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for CustomerDealsHistory model.

    Allows conversion of CustomerDealsHistory objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - car (ForeignKey) - car on sale.
        - amount (PositiveIntegerField) - amount of selling cars.
        - price_per_one (BigIntegerField) - price per 1 car qty.
        - date (DateTimeField) - date of the deal.
        - customer (ForeignKey) - represents customer in deal.
        - dealer (ForeignKey) - represents dealer in deal.
    """

    class Meta:
        model = CustomerDealsHistory
        fields = [
            "pk",
            "car",
            "amount",
            "price_per_one",
            "date",
            "customer",
            "dealer",
        ]


class DealerDealsHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for DealerDealsHistory model.

    Allows conversion of DealerDealsHistory objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - car (ForeignKey) - car on sale.
        - amount (PositiveIntegerField) - amount of selling cars.
        - price_per_one (BigIntegerField) - price per 1 car qty.
        - date (DateTimeField) - date of the deal.
        - dealer (ForeignKey) - represents dealer in deal.
        - supplier (ForeignKey) - represents supplier in deal.
    """

    class Meta:
        model = DealerDealsHistory
        fields = [
            "pk",
            "car",
            "amount",
            "price_per_one",
            "date",
            "dealer",
            "supplier",
        ]


class TotalDealerPurchaseSerializer(serializers.ModelSerializer):
    """
    Serializer for TotalDealerPurchase model.

    Allows conversion of TotalDealerPurchase objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - customer (ForeignKey) - represents customer as buyer.
        - dealer (ForeignKey) - represents dealer as seller.
        - amount (PositiveBigIntegerField) - total amount of cars sold to customer.
    """

    class Meta:
        model = TotalDealerPurchase
        fields = [
            "pk",
            "customer",
            "dealer",
            "amount",
        ]


class TotalSupplierPurchaseSerializer(serializers.ModelSerializer):
    """
    Serializer for TotalSupplierPurchase model.

    Allows conversion of TotalSupplierPurchase objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - dealer (ForeignKey) - represents dealer as buyer.
        - supplier (ForeignKey) - represents customer as seller.
        - amount (PositiveBigIntegerField) - total amount of cars sold to customer.
    """

    class Meta:
        model = TotalSupplierPurchase
        fields = [
            "pk",
            "dealer",
            "supplier",
            "amount",
        ]
