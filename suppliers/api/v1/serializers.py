from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from cars.api.v1.serializers import CarSerializer
from cars.models import Car

from suppliers.models import Supplier, SupplierStockItem


class SupplierSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for Supplier model.

    Allows conversion of Supplier objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Supplier model.
        - name (CharField) - company name.
        - place (CountryField) - company location.
        - foundation_date (DateField, optional) - date of company foundation.
    """

    class Meta:
        model = Supplier
        fields = ["pk", "name", "place", "foundation_date"]


class SupplierOwnerSerializer(SupplierSerializer):
    """
    Serializer for Supplier model.

    Inherits from SupplierSerializer.
    Serializer shows balance field only for user who is supplier owner.

    Allows conversion of Supplier objects to/from JSON format.
    Parameters:
        - place (CountryField) - company location.
    """

    class Meta:
        model = Supplier
        fields = SupplierSerializer.Meta.fields + ["balance"]


class SupplierStockItemSerializer(serializers.ModelSerializer):
    """
    Serializer for SupplierStockItem model.

    Allows conversion of Supplier objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for SupplierStockItem model.
        - amount (ForeignKey) - amount of cars on stock.
        - price_per_one (DecimalField) - price per one car.
        - car (ForeignKey) - relation to Car table. Represents car item on stock.
        - supplier (ForeignKey) - relation to Supplier table. Represents owner of stock item.
    """

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), required=False
    )
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())

    class Meta:
        model = SupplierStockItem
        fields = ["pk", "amount", "price_per_one", "car", "supplier"]
