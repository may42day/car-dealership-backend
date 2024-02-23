from django.db import models

from cars.validators import (
    validate_car_characteristic_year_sequence,
    validate_car_year_sequence,
)
from common.models import AmountCalculator, BaseModel


class CarCharacteristic(BaseModel):
    """
    A class to represent a car characteristics entry.
    Used for storing car characteristics which will be selling by dealers.
    Inherits from class BaseModel.

    Attributes
    ----------
    brand : CharField
        car brand (e.g. Chevrolet)
    car_model : CharField
        car model/product line (e.g. Camaro)
    generation : CharField
        car generation (e.g. 2nd-Gen)
    year_release : PositiveSmallIntegerField
        start date of car production (e.g. 1970)
    year_end_of_production : PositiveSmallIntegerField
        end date of car production (e.g. 1981)
    """

    brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255, null=True, blank=True)
    generation = models.CharField(max_length=255, null=True, blank=True)
    year_release = models.PositiveSmallIntegerField(null=True, blank=True)
    year_end_of_production = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.brand} {self.car_model} {self.generation}"

    def clean(self, *args, **kwargs):
        validate_car_characteristic_year_sequence(
            self.year_release, self.year_end_of_production
        )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_suitable(self, characteristic: "CarCharacteristic"):
        """
        Function checking if current characteristic suitable for another.

        Two characteristics will be suiatable if all existing fields of first one
        will be equal to fields of another characteristic.
        """
        if characteristic.brand and characteristic.brand != self.brand:
            return False
        elif characteristic.car_model and characteristic.car_model != self.car_model:
            return False
        elif characteristic.generation and characteristic.generation != self.generation:
            return False
        elif (
            characteristic.year_release
            and characteristic.year_release != self.year_release
        ):
            return False
        elif (
            characteristic.year_end_of_production
            and characteristic.year_end_of_production != self.year_end_of_production
        ):
            return False
        return True


class Car(BaseModel):
    """
    A class to represent a car entry.
    Inherits from class BaseModel.

    Attributes
    ----------
    brand : CharField
        car brand (e.g. Chevrolet)
    car_model : CharField
        car model/product line (e.g. Camaro)
    generation : CharField
        car generation (e.g. 2nd-Gen)
    year_release : PositiveSmallIntegerField
        start date of car production (e.g. 1970)
    year_end_of_production : PositiveSmallIntegerField
        end date of car production (e.g. 1981)
    """

    brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    generation = models.CharField(max_length=255, default=1)
    year_release = models.PositiveSmallIntegerField()
    year_end_of_production = models.PositiveSmallIntegerField(
        null=True, blank=True, default=None
    )

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of brand name, car model and it's generation
        """
        return f"{self.brand} {self.car_model} {self.generation}"

    def clean(self, *args, **kwargs):
        validate_car_year_sequence(self.year_release, self.year_end_of_production)
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_fit_characteristic(self, characteristic: CarCharacteristic) -> bool:
        """
        Function to check wether car fit with car characteristic.
        """
        if characteristic.brand and characteristic.brand != self.brand:
            return False
        elif characteristic.car_model and characteristic.car_model != self.car_model:
            return False
        elif characteristic.generation and characteristic.generation != self.generation:
            return False
        elif (
            characteristic.year_release
            and characteristic.year_release != self.year_release
        ):
            return False
        elif (
            characteristic.year_end_of_production
            and characteristic.year_end_of_production != self.year_end_of_production
        ):
            return False
        return True


class CarStockItem(AmountCalculator, BaseModel):
    """
    An abstract class to represent a stock item of cars.
    Related to :model:'cars.Car'
    Inherits from class BaseModel.

    Attributes
    ----------
    car : ForeignKey
        relation to Car table
    amount : PositiveIntegerField
        amount of specific car on stock
    price_per_one : DecimalField
        car price for 1 qty
    """

    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    price_per_one = models.PositiveBigIntegerField()

    class Meta:
        abstract = True

    def is_fit_characteristic(self, characteristic: CarCharacteristic) -> bool:
        return self.car.is_fit_characteristic(characteristic)

    def __str__(self) -> str:
        """
        Represents str model name

        Returns:
            str: name consists of car brand, model and its amount on stock
        """
        return f"{self.car.brand} {self.car.car_model} ({self.amount})"
