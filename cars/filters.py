from django_filters import rest_framework as filters
import django_filters

from cars.models import Car, CarCharacteristic


class CarFilter(filters.FilterSet):
    """
    A filter class for filtering Car objects by different options.

    Filters
    -------
    - year_release__gt: Filter cars with release year is grater than specified value.
    - year_end_of_production__lt: Filter cars with end of production year is less than specified value.
    - in_production: Filter cars that are in production now (year_end_of_production is None).
    - brand: Filter cars by brand name (exact match, case-insensitive).
    - car_model: Filter cars by car model (partial match, case-insensitive).
    - generation: Filter cars by car generation (partial match, case-insensitive).
    """

    year_release__gt = django_filters.NumberFilter(
        field_name="year_release", lookup_expr="gt"
    )
    year_end_of_production__lt = django_filters.NumberFilter(
        field_name="year_end_of_production", lookup_expr="lt"
    )
    in_production = django_filters.BooleanFilter(
        field_name="year_end_of_production", lookup_expr="isnull"
    )

    class Meta:
        model = Car
        fields = {
            "brand": ["iexact"],
            "car_model": ["icontains"],
            "generation": ["icontains"],
        }


class CarCharacteristicFilter(CarFilter):
    """
    A filter class for filtering Car characteristic objects by different options.

    Inherits from CarFilter and override Meta class with CarCharacteristic model.
    """

    class Meta:
        model = CarCharacteristic
        fields = {
            "brand": ["iexact"],
            "car_model": ["icontains"],
            "generation": ["icontains"],
        }
