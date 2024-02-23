from django.forms import ValidationError

from datetime import datetime

ERROR_MESSAGE_YEARS_SEQUENCE = "Error years sequence"
ERROR_MESSAGE_CURRENT_YEAR = (
    "Error years. Release year must be smaller than current year"
)


def validate_car_year_sequence(year_release: int, year_end_of_production: int):
    """
    Function to validate years sequence.
    Comparing two years and checks whether end of production year goes after release year.
    If following year is null it means the car is still in production.
    Also checks if end of production year is before current year.
    """
    current_year = datetime.now().year

    if year_end_of_production and year_release > year_end_of_production:
        raise ValidationError(ERROR_MESSAGE_YEARS_SEQUENCE)
    elif year_release > current_year:
        raise ValidationError(ERROR_MESSAGE_CURRENT_YEAR)


def validate_car_characteristic_year_sequence(
    year_release: int, year_end_of_production: int
):
    """
    Function to validate years sequence.
    Comparing two years if they are not null and checks whether end of production year goes after release year.
    If following year is null it means the car is still in production.
    Also checks if end of production year is before current year.
    """
    current_year = datetime.now().year

    if year_release and year_release > current_year:
        raise ValidationError(ERROR_MESSAGE_CURRENT_YEAR)
    elif year_end_of_production and year_end_of_production > current_year:
        raise ValidationError(ERROR_MESSAGE_CURRENT_YEAR)
    elif (year_release and year_end_of_production) and (
        year_release > year_end_of_production
    ):
        raise ValidationError(ERROR_MESSAGE_YEARS_SEQUENCE)
