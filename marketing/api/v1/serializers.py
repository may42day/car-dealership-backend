from rest_framework import serializers

from cars.api.v1.serializers import CarSerializer
from dealers.models import Dealer
from marketing.models import (
    DealerDiscount,
    SupplierDiscount,
    DealerMarketingCampaign,
    SupplierMarketingCampaign,
)
from suppliers.models import Supplier


class DealerDiscountSerializer(serializers.ModelSerializer):
    """
    Serializer for DealerDiscount model.

    Allows conversion of DealerDiscount objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - name (CharField) - name of discount.
        - min_amount (PositiveIntegerField) - minimal quantity the discount will act from.
        - percentage (DecimalField) - percenate of discount.
        - discount_type (CharField, choices) - type of discount (store one of the choices: BD/CD).
        - dealer (ForeignKey) - represents dealer who is discount owner
    """

    dealer = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(), required=False
    )

    class Meta:
        model = DealerDiscount
        fields = ["pk", "name", "min_amount", "percentage", "discount_type", "dealer"]


class SupplierDiscountSerializer(serializers.ModelSerializer):
    """
    Serializer for SupplierDiscount model.

    Allows conversion of SupplierDiscount objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - name (CharField) - name of discount.
        - min_amount (PositiveIntegerField) - minimal quantity the discount will act from.
        - percentage (DecimalField) - percenate of discount.
        - discount_type (CharField, choices) - type of discount (store one of the choices: BD/CD).
        - supplier (ForeignKey) - represents supplier who is discount owner
    """

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), required=False
    )

    class Meta:
        model = SupplierDiscount
        fields = ["pk", "name", "min_amount", "percentage", "discount_type", "supplier"]


class DealerMarketingCampaignSerializer(serializers.ModelSerializer):
    """
    Serializer for DealerMarketingCampaign model.

    Allows conversion of DealerMarketingCampaign objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - name (CharField) - name of campaign.
        - description (TextField) - description with event details.
        - percentage (DecimalField) - percenate of discount for every car.
        - start_date (DateTimeField) - start date of campagin.
        - end_date (DateTimeField) - end date of campagin.
        - dealer (ForeignKey) - represents supplier who is marketing campaign owner.
        - cars (ManyToManyField, read-only) - cars which participate in event.
    """

    cars = CarSerializer(many=True, read_only=True)
    dealer = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(), required=False
    )

    class Meta:
        model = DealerMarketingCampaign
        fields = [
            "pk",
            "name",
            "description",
            "percentage",
            "cars",
            "start_date",
            "end_date",
            "dealer",
        ]


class SupplierMarketingCampaignSerializer(serializers.ModelSerializer):
    """
    Serializer for SupplierMarketingCampaign model.

    Allows conversion of SupplierMarketingCampaign objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - name (CharField) - name of campaign.
        - description (TextField) - description with event details.
        - percentage (DecimalField) - percenate of discount for every car.
        - start_date (DateTimeField) - start date of campagin.
        - end_date (DateTimeField) - end date of campagin.
        - supplier (ForeignKey) - represents supplier who is marketing campaign owner.
        - cars (ManyToManyField, read-only) - cars which participate in event.
    """

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), required=False
    )
    cars = CarSerializer(many=True, read_only=True)

    class Meta:
        model = SupplierMarketingCampaign
        fields = [
            "pk",
            "name",
            "description",
            "percentage",
            "cars",
            "start_date",
            "end_date",
            "supplier",
        ]
