import pytest
from ddf import G
from cars.models import Car, CarCharacteristic
from cars.validators import ERROR_MESSAGE_CURRENT_YEAR, ERROR_MESSAGE_YEARS_SEQUENCE


@pytest.mark.django_db
class TestCarModel:
    """
    Test class for car model.
    """

    def test_cars_years_validation_should_panic(self):
        """
        Checking whether invalid year sequence panics
        """
        with pytest.raises(Exception, match=ERROR_MESSAGE_YEARS_SEQUENCE):
            _car = G(
                Car,
                brand="Chevrolet",
                car_model="Corvette",
                generation="C7",
                year_release=2018,
                year_end_of_production=2014,
            )

    def test_cars_years_validation_should_panic2(self):
        """
        Checking whether invalid year which is bigger than current year panics
        """
        with pytest.raises(Exception, match=ERROR_MESSAGE_CURRENT_YEAR):
            _car = G(
                Car,
                brand="Chevrolet",
                car_model="Corvette",
                generation="C7",
                year_release=2050,
            )

    def test_cars_years_validation_should_not_panic(self):
        """
        Checking whether valid sequence not panics
        """
        try:
            _car = G(
                Car,
                brand="Chevrolet",
                car_model="Corvette",
                generation="C7",
                year_release=2014,
                year_end_of_production=2018,
            )
            assert True
        except Exception:
            assert False


@pytest.mark.django_db
class TestCarCharacteristic:
    """
    Test class for car characteristic model.
    """

    def test_cars_characteristic_years_validation_should_panic(self):
        """
        Checking whether invalid year sequence panics
        """
        with pytest.raises(Exception, match=ERROR_MESSAGE_YEARS_SEQUENCE):
            _car_characteristic = G(
                CarCharacteristic,
                brand="Chevrolet",
                car_model="Corvette",
                generation="C7",
                year_release=2018,
                year_end_of_production=2014,
            )

    def test_cars_characteristic_years_validation_should_panic2(self):
        """
        Checking whether invalid year which is bigger than current year panics
        """
        with pytest.raises(Exception, match=ERROR_MESSAGE_CURRENT_YEAR):
            _car_characteristic = G(
                CarCharacteristic,
                brand="Chevrolet",
                car_model="Corvette",
                generation="C7",
                year_release=2050,
            )

    def test_cars_characteristic_years_validation_should_not_panic(self):
        """
        Checking whether valid sequence not panics
        """
        try:
            _car_characteristic = G(
                CarCharacteristic,
                brand="Chevrolet",
                car_model="Corvette",
                generation="C7",
                year_release=2014,
                year_end_of_production=2018,
            )
            assert True
        except Exception:
            assert False

    def test_suitable_characteristics(self):
        """
        Checking whether two simillar characteristics fits each other
        """
        car_characteristic1 = G(
            CarCharacteristic,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C7",
            year_release=2014,
            year_end_of_production=2018,
        )

        car_characteristic2 = G(
            CarCharacteristic,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C7",
        )

        is_suitable = car_characteristic1.is_suitable(car_characteristic2)
        assert is_suitable

    def test_suitable_characteristics2(self):
        """
        Checking whether two simillar characteristics fits each other
        """
        car_characteristic1 = G(
            CarCharacteristic,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C7",
            year_release=2014,
            year_end_of_production=2018,
        )
        car_characteristic2 = G(
            CarCharacteristic,
            brand="Chevrolet",
            generation="C7",
        )
        is_suitable = car_characteristic1.is_suitable(car_characteristic2)
        assert is_suitable

    def test_not_suitable_characteristics(self):
        """
        Checking whether two simillar characteristics doesn't fit each other
        """
        car_characteristic1 = G(
            CarCharacteristic,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C7",
            year_release=2014,
            year_end_of_production=2018,
        )

        car_characteristic2 = G(
            CarCharacteristic,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C7",
            year_release=2014,
            year_end_of_production=2020,
        )

        is_suitable = car_characteristic1.is_suitable(car_characteristic2)
        assert not is_suitable

    def test_car_fit_characteristic(self):
        """
        Checking whether car fits with specific characteristic
        """
        car_characteristic = G(
            CarCharacteristic,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C7",
        )
        car = G(
            Car,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C7",
            year_release=2014,
            year_end_of_production=2018,
        )
        is_fit = car.is_fit_characteristic(car_characteristic)
        assert is_fit

    def test_car_not_fit_characteristic(self):
        """
        Checking whether car doesn't fit with specific characteristic
        """
        car_characteristic = G(
            CarCharacteristic,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C8",
        )

        car = G(
            Car,
            brand="Chevrolet",
            car_model="Corvette",
            generation="C7",
            year_release=2014,
            year_end_of_production=2018,
        )
        is_fit = car.is_fit_characteristic(car_characteristic)
        assert not is_fit
