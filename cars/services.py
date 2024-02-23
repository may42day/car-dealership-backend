from django.db.models import Q

from cars.models import Car, CarCharacteristic


def pick_up_car_by_characteristic(
    characteristic: CarCharacteristic, cars: list[Car], exact_match: bool = False
) -> list[Car]:
    """
    Function for searching for cars by car characteristic.
    """
    q_filters = Q()

    if characteristic.brand:
        if exact_match:
            q_filters &= Q(brand=characteristic.brand)
        else:
            q_filters &= Q(brand__contains=characteristic.brand)

    if characteristic.car_model:
        if exact_match:
            q_filters &= Q(car_model=characteristic.car_model)
        else:
            q_filters &= Q(car_model__contains=characteristic.car_model)

    if characteristic.generation:
        if exact_match:
            q_filters &= Q(generation=characteristic.generation)
        else:
            q_filters &= Q(generation__contains=characteristic.generation)

    if characteristic.year_release:
        q_filters &= Q(year_release=characteristic.year_release)

    if characteristic.year_end_of_production:
        q_filters &= Q(year_end_of_production=characteristic.year_end_of_production)

    cars = Car.objects.all()
    filtered_cars_queryset = cars.filter(q_filters)
    return filtered_cars_queryset
