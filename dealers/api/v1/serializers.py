from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from cars.api.v1.serializers import CarCharacteristicSerializer
from suppliers.api.v1.serializers import SupplierSerializer
from customers.api.v1.serializers import CustomerSerializer
from dealers.models import Dealer, DealerStockItem


class DealerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for Dealer model.

    Serializer shows balance, customers, suppliers field only for user who is supplier owner.

    Allows conversion of Dealer objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Supplier model.
        - name (CharField) - company name.
        - place (CountryField) - company location.
        - foundation_date (DateField, optional) - date of company foundation.
        - car_characteristics (CarCharacteristicSerializer, read-only) - represents characteristics of cars for sale
    """

    car_characteristics = CarCharacteristicSerializer(many=True, read_only=True)

    class Meta:
        model = Dealer
        fields = [
            "name",
            "place",
            "foundation_date",
            "car_characteristics",
        ]


class DealerOwnerSerializer(DealerSerializer):
    """
    Serializer for Dealer model.

    Inherits from DealerSerializer.
    Serializer shows balance, customers, suppliers field only for user who is supplier owner.

    Allows conversion of Dealer objects to/from JSON format.
    Parameters:
        - balance (PositiveBigIntegerField) - current company's balance.
        - customers (CustomerSerializer, read-only) - represents dealer's customers.
        - suppliers (SupplierSerializer, read-only) - represents dealer's suppliers.
    """

    customers = CustomerSerializer(many=True, read_only=True)
    suppliers = SupplierSerializer(many=True, read_only=True)
    car_characteristics = CarCharacteristicSerializer(many=True, read_only=True)

    class Meta:
        model = Dealer
        fields = DealerSerializer.Meta.fields + [
            "balance",
            "customers",
            "suppliers",
        ]
        read_only_fields = ["balance"]


class DealerStockItemSerializer(serializers.ModelSerializer):
    """
    Serializer for SupplierStockItem model.

    Allows conversion of Supplier objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for SupplierStockItem model.
        - amount (ForeignKey) - amount of cars on stock.
        - price_per_one (DecimalField) - price per one car.
        - car (ForeignKey) - relation to Car table. Represents car item on stock.
        - dealer (ForeignKey) - relation to Supplier table. Represents owner of stock item.
    """

    dealer = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(), required=False
    )

    class Meta:
        model = DealerStockItem
        fields = ["pk", "amount", "price_per_one", "car", "dealer"]
