import pytest
from ddf import G
from cars.api.v1.serializers import CarSerializer
from cars.models import Car, CarCharacteristic


@pytest.fixture
def car_data():
    """
    Fixture with car data to check filters.
    """
    car1 = G(Car, brand="Car#1 Test", year_release=2015, year_end_of_production=2020)
    car2 = G(Car, car_model="Car#11", year_release=2014, year_end_of_production=2019)
    car3 = G(Car, year_release=2013)
    car4 = G(Car, year_release=2012)

    return {
        "car1": car1,
        "car2": car2,
        "car3": car3,
        "car4": car4,
    }


@pytest.fixture
def car_characteristic_data():
    """
    Fixture with car characteristic data to check filters.
    """
    car_characteristic1 = G(
        CarCharacteristic,
        brand="Car#1 Test",
        year_release=2015,
        year_end_of_production=2020,
    )
    car_characteristic2 = G(
        CarCharacteristic,
        car_model="Car#11",
        year_release=2014,
        year_end_of_production=2019,
    )
    car_characteristic3 = G(CarCharacteristic, year_release=2013)
    car_characteristic4 = G(CarCharacteristic, year_release=2012)

    return {
        "car_characteristic1": car_characteristic1,
        "car_characteristic2": car_characteristic2,
        "car_characteristic3": car_characteristic3,
        "car_characteristic4": car_characteristic4,
    }


@pytest.mark.django_db
class TestCarFilters:
    """
    Test Car and Car characteristics filters.
    """

    @pytest.mark.parametrize(
        "fixture_data_dict_prefix, fixture_data_name, url",
        [
            ("car", "car_data", "/api/v1/cars/"),
            (
                "car_characteristic",
                "car_characteristic_data",
                "/api/v1/cars/characteristics/",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "fixture_data_dict_postfix, query_param, query_value",
        [
            (["4", "3", "2", "1"], "ordering", "year_release"),
            (["1", "2", "3", "4"], "ordering", "-year_release"),
            (["2", "1", "3", "4"], "ordering", "year_end_of_production"),
            (["3", "4", "1", "2"], "ordering", "-year_end_of_production"),
            (["3", "4"], "in_production", True),
            (["1", "2"], "in_production", False),
            (["1", "2"], "year_release__gt", 2013),
            (["2"], "year_end_of_production__lt", 2020),
            (["1", "2"], "search", "Car#1"),
            (["1"], "brand__iexact", "Car#1 Test"),
        ],
    )
    def test_cars_ordering(
        self,
        api_client,
        fixture_data_name,
        query_param,
        query_value,
        fixture_data_dict_prefix,
        fixture_data_dict_postfix,
        url,
        request,
        car_characteristic_data,
        car_data,
    ):
        """
        Checks filter ordering by years of release and end of production.
        """
        data = {
            query_param: query_value,
        }
        response = api_client.get(url, data=data, format="json")
        dict_data = request.getfixturevalue(fixture_data_name)
        serializer_data = CarSerializer(
            [
                dict_data[f"{fixture_data_dict_prefix}{postfix}"]
                for postfix in fixture_data_dict_postfix
            ],
            many=True,
        ).data

        assert response.data == serializer_data
