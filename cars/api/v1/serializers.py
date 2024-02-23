from rest_framework import serializers

from cars.models import Car, CarCharacteristic


class CarSerializer(serializers.ModelSerializer):
    """
    Serializer for Car model.

    Allows conversion of Car objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - brand (CharField) - car brand.
        - car_model (CharField) - car model/product line.
        - generation (CharField) - car generation.
        - year_release (PositiveSmallIntegerField) - start date of car production.
        - year_end_of_production (PositiveSmallIntegerField, optional) - end date of car production.

    Used in:
        - [cars] CarAPIView. Used for serializing Car objects.
        - [customers] CustomerSerializer. Used for representing customers cars.
        - [customers] CustomerCarsListAPIView. Used for representing customers cars.
        - [marketing] DealerMarketingCampaignSerializer. Used for representing cars which participate in camaign.
    """

    class Meta:
        model = Car
        fields = [
            "pk",
            "brand",
            "car_model",
            "generation",
            "year_release",
            "year_end_of_production",
        ]


class CarCharacteristicSerializer(serializers.ModelSerializer):
    """
    Serializer for CarCharacteristic model.

    Allows conversion of CarCharacteristic objects to/from JSON format.
    Parameters:
        - pk (int) - Primary Key for Car model.
        - brand (CharField) - car brand.
        - car_model (CharField, optional) - car model/product line.
        - generation (CharField, optional) - car generation.
        - year_release (PositiveSmallIntegerField, optional) - start date of car production.
        - year_end_of_production (PositiveSmallIntegerField, optional) - end date of car production.

    Used in:
        - [cars] CarCharacteristicAPIView. Used for serializing CarCharacteristic objects.
        - [dealers] DealerSerializer. Used for dealers car characteristics which represents dealer cars for sale.
    """

    class Meta:
        model = CarCharacteristic
        fields = [
            "pk",
            "brand",
            "car_model",
            "generation",
            "year_release",
            "year_end_of_production",
        ]
