from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from cars.api.v1.serializers import CarSerializer
from customers.models import Customer


class CustomerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for Customer model.

    Allows conversion of Customer objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - name (CharField) - name of customer.
        - place (CountryField) - customer location.

    Used in:
        - [customers] CustomerAPIView. Used for serializing Customer objects.
        - [dealers] DealerSerializer. Used for representig dealer customers.
    """

    class Meta:
        model = Customer
        fields = ["pk", "name", "place"]


class CustomerOwnerSerializer(CustomerSerializer):
    """
    Serializer for Customer model only for owners.
    Inherits from CustomerSerializer

    Allows conversion of Customer objects to/from JSON format.
    Parameters:
        - balance (PositiveBigIntegerField) - customer balance.
        - place (CountryField) - customer location.
        - created_at (DateTimeField) - customer registration data.

    Used in:
        - [customers] CustomerAPIView. Used for serializing Customer objects.
        - [dealers] DealerSerializer. Used for representig dealer customers.
    """

    cars = CarSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = CustomerSerializer.Meta.fields + ["balance", "cars", "created_at"]
        read_only_fields = ["balance", "cars", "created_at"]
