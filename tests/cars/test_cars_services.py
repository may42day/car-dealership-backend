from ddf import G
import pytest
from cars.models import Car, CarCharacteristic
from cars.services import pick_up_car_by_characteristic


@pytest.mark.django_db
def test_pick_up_car_by_characteristic():
    """
    Checking correct picking up the cars by car characteristics
    """
    characteristic = G(CarCharacteristic, brand="Chevrolet", car_model="Corvette")
    car1 = G(
        Car,
        brand="Chevrolet",
        car_model="Corvette",
        generation="C7",
        year_release=2014,
    )
    car2 = G(
        Car,
        brand="Chevrolet",
        car_model="Corvette",
        generation="C6",
        year_release=2007,
        year_end_of_production=2014,
    )
    car3 = G(
        Car,
        brand="Chevrolet Corvette",
        car_model="Corvette С6",
        generation="С6",
        year_release=2013,
    )
    car4 = G(
        Car,
        brand="Dodge",
        car_model="Charger",
        generation="LD",
        year_release=2014,
    )
    all_cars = [car1, car2, car3, car4]

    exact_match = True
    cars = pick_up_car_by_characteristic(characteristic, all_cars, exact_match)
    assert car1 in cars
    assert car2 in cars
    assert car3 not in cars
    assert car4 not in cars

    exact_match = False
    cars = pick_up_car_by_characteristic(characteristic, all_cars, exact_match)
    assert car1 in cars
    assert car2 in cars
    assert car3 in cars
    assert car4 not in cars
