import pytest
from ddf import G

from django.test.utils import CaptureQueriesContext
from django.db import connection

from cars.models import Car, CarCharacteristic
from customers.models import Customer
from dealers.models import Dealer, DealerStockItem
from marketing.models import DealerDiscount, DealerMarketingCampaign
from orders.models import CustomerOffer, TotalDealerPurchase
from orders.offer_handler import CustomersOfferHandler
from orders.tasks import handle_customer_offer
from tests.conftest import parse_captured_queries_context


@pytest.mark.django_db
class TestOfferValidation:
    """
    Test class for offers validation.
    """

    def test_offer_not_valid(self):
        """
        Checking whether offer with invalid car characteristic isn't valid
        """
        customer = G(Customer)
        not_valid_characteristic = G(
            CarCharacteristic, brand="brand", car_model="car model"
        )
        offer = G(
            CustomerOffer, customer=customer, characteristic=not_valid_characteristic
        )
        is_valid = offer.is_valid_for_offer()
        assert is_valid is False

    def test_offer_valid(self):
        """
        Checking whether offer with valid car characteristic is valid
        """
        customer = G(Customer)
        valid = G(
            CarCharacteristic, brand="brand", car_model="car model", generation="1"
        )
        offer = G(CustomerOffer, customer=customer, characteristic=valid)
        is_valid = offer.is_valid_for_offer()
        assert is_valid is True

    def test_offer_not_valid2(self):
        """
        Checking whether offer with characteristic and car in the same time isn't valid.
        """
        customer = G(Customer)
        car = G(Car)
        valid_characteristic = G(
            CarCharacteristic,
            brand="brand",
            car_model="car model",
            generation="1",
        )
        offer = G(
            CustomerOffer,
            customer=customer,
            characteristic=valid_characteristic,
            car=car,
        )
        is_valid = offer.is_valid_for_offer()
        assert is_valid is False

    def test_offer_not_valid3(self):
        """
        Checking whether offer with no characteristic and car in the same time isn't valid.
        """
        customer = G(Customer)
        offer = G(
            CustomerOffer,
            customer=customer,
        )
        is_valid = offer.is_valid_for_offer()
        assert is_valid is False


@pytest.fixture
def offer_handler_data() -> dict:
    """
    Data for testing offer handler.
    """
    customer = G(Customer, balance=10000)
    offer_characteristic = G(
        CarCharacteristic, brand="Brand1", car_model="Model1", generation="1"
    )
    offer_with_characteristic = G(
        CustomerOffer,
        customer=customer,
        characteristic=offer_characteristic,
        max_price=1000,
    )

    dealer_characteristic1 = G(CarCharacteristic, brand="Brand1")
    dealer_characteristic2 = G(CarCharacteristic, brand="Brand1", car_model="Model1")
    dealer_characteristic3 = G(
        CarCharacteristic, brand="Brand1", car_model="Model1", generation="1"
    )
    dealer_characteristic4 = G(
        CarCharacteristic, brand="Brand2", car_model="Model1", generation="1"
    )

    car1 = G(Car, brand="Brand1", car_model="Model1", generation="1")
    offer_with_car = G(CustomerOffer, customer=customer, car=car1, max_price=1000)

    car2 = G(Car, brand="Brand1", car_model="Model1", generation="2")
    car3 = G(Car, brand="Brand3", car_model="Model3", generation="3")

    dealer1 = G(
        Dealer,
        car_characteristics=[dealer_characteristic1, dealer_characteristic3],
        balance=500000,
    )
    dealer1_stock1 = G(
        DealerStockItem, dealer=dealer1, car=car1, amount=50, price_per_one=500
    )
    _dealer1_stock2 = G(
        DealerStockItem, dealer=dealer1, car=car2, amount=999, price_per_one=600
    )
    _dealer1_stock3 = G(
        DealerStockItem, dealer=dealer1, car=car3, amount=999, price_per_one=600
    )
    _dealer1_stock4 = G(
        DealerStockItem, dealer=dealer1, car=car1, amount=999, price_per_one=510
    )

    dealer2 = G(Dealer, car_characteristics=[dealer_characteristic1])
    _dealer2_stock1 = G(
        DealerStockItem, dealer=dealer2, car=car1, amount=1, price_per_one=490
    )
    _dealer2_stock2 = G(
        DealerStockItem, dealer=dealer2, car=car2, amount=999, price_per_one=200
    )
    _dealer2_stock3 = G(
        DealerStockItem, dealer=dealer2, car=car3, amount=999, price_per_one=600
    )

    dealer3 = G(Dealer, car_characteristics=[dealer_characteristic2])
    _dealer3_stock1 = G(
        DealerStockItem, dealer=dealer3, car=car1, amount=999, price_per_one=501
    )
    _dealer3_stock2 = G(
        DealerStockItem, dealer=dealer3, car=car2, amount=999, price_per_one=300
    )
    _dealer3_stock3 = G(
        DealerStockItem, dealer=dealer3, car=car3, amount=999, price_per_one=600
    )
    _dealer3_stock4 = G(
        DealerStockItem, dealer=dealer3, car=car1, amount=1, price_per_one=800
    )

    dealer4 = G(Dealer, car_characteristics=[dealer_characteristic4])
    _dealer4_stock1 = G(
        DealerStockItem, dealer=dealer4, car=car3, amount=999, price_per_one=222
    )

    _dealer1_discount1 = G(
        DealerDiscount,
        dealer=dealer1,
        discount_type="CD",
        min_amount=5,
        percentage=5,
    )
    _dealer1_discount2 = G(
        DealerDiscount,
        dealer=dealer1,
        discount_type="BD",
        min_amount=10,
        percentage=8,
    )
    _dealer2_discount = G(
        DealerDiscount,
        dealer=dealer2,
        discount_type="CD",
        min_amount=8,
        percentage=3,
    )
    _dealer3_discount = G(
        DealerDiscount,
        dealer=dealer3,
        discount_type="CD",
        min_amount=20,
        percentage=20,
    )

    _total_purchases_dealer1 = G(
        TotalDealerPurchase, dealer=dealer1, customer=customer, amount=10
    )
    _total_purchases_dealer2 = G(
        TotalDealerPurchase, dealer=dealer2, customer=customer, amount=10
    )

    _dealer1_marketing_campaign1 = G(
        DealerMarketingCampaign,
        dealer=dealer1,
        percentage=0,
        cars=[car1, car2, car3],
    )
    _dealer1_marketing_campaign2 = G(
        DealerMarketingCampaign, dealer=dealer1, percentage=5, cars=[car1]
    )
    _dealer2_marketing_campaign1 = G(
        DealerMarketingCampaign, dealer=dealer2, percentage=3, cars=[car1]
    )
    _dealer3_marketing_campaign1 = G(
        DealerMarketingCampaign, dealer=dealer3, percentage=5, cars=[car3]
    )
    _dealer4_marketing_campaign1 = G(
        DealerMarketingCampaign, dealer=dealer4, percentage=55, cars=[car3]
    )

    data = {
        "customer": customer,
        "dealers": [dealer1, dealer2, dealer3, dealer4],
        "offer_with_characteristic": offer_with_characteristic,
        "offer_with_car": offer_with_car,
        "choosed_car": car1,
        "choosed_dealer": dealer1,
        "dealer1_stock1": dealer1_stock1,
    }
    return data


class TestOfferHandler:
    @pytest.mark.dependency()
    @pytest.mark.django_db
    def test_offer_with_characteristics_sellers_with_suitable_characteristics(
        self, offer_handler_data: dict
    ):
        """
        Checking whether offer handler correctly picks up dealers by characteristics
        """
        dealers = offer_handler_data["dealers"]
        offer = offer_handler_data["offer_with_characteristic"]
        handler = CustomersOfferHandler(offer, dealers)
        handler._sellers_with_suitable_characteristics()
        assert dealers[0] in handler.sellers
        assert dealers[1] in handler.sellers
        assert dealers[2] in handler.sellers
        assert dealers[3] not in handler.sellers

    @pytest.mark.django_db
    def test_offer_with_characteristics_dealers_with_stock_items(
        self, offer_handler_data: dict
    ):
        """
        Checking whether offer handler correctly picks up dealers by their stock items
        in comparison with car in offer.
        """
        dealers = offer_handler_data["dealers"]
        offer = offer_handler_data["offer_with_characteristic"]
        handler = CustomersOfferHandler(offer, dealers)
        handler._sellers_suitable_stock_items_by_characteristics()

        dealers_data = handler.sellers_data
        assert dealers_data
        assert dealers[0].pk in dealers_data
        assert dealers[1].pk in dealers_data
        assert dealers[2].pk in dealers_data
        assert dealers[3].pk not in dealers_data

        assert len(dealers_data[dealers[0].pk]["suitable_stock"]) == 2
        assert len(dealers_data[dealers[1].pk]["suitable_stock"]) == 1
        assert len(dealers_data[dealers[2].pk]["suitable_stock"]) == 2

    @pytest.mark.django_db
    def test_offer_with_characteristics_seller_best_stock_item(
        self, offer_handler_data: dict
    ):
        """
        Checking whether offer handler correctly picks up best stock item for every dealer
        """
        dealers = offer_handler_data["dealers"]
        offer = offer_handler_data["offer_with_characteristic"]
        handler = CustomersOfferHandler(offer, dealers)
        handler._sellers_suitable_stock_items_by_characteristics()
        handler._seller_best_stock_item()

        dealers_data = handler.sellers_data
        assert dealers_data
        assert dealers[0].pk in dealers_data

        assert dealers_data[dealers[0].pk]["best_stock_item"].amount == 50
        assert dealers_data[dealers[0].pk]["best_stock_item"].price_per_one == 500

    @pytest.mark.django_db
    def test_offer_with_characteristics_seller_suitable_discounts(
        self, offer_handler_data: dict
    ):
        """
        Checking whether offer handler correctly picks up discounts for every dealer
        """
        dealers = offer_handler_data["dealers"]
        offer = offer_handler_data["offer_with_characteristic"]
        handler = CustomersOfferHandler(offer, dealers)
        handler._sellers_with_suitable_characteristics()
        handler._sellers_suitable_stock_items_by_characteristics()
        handler._seller_suitable_discounts()

        dealers_data = handler.sellers_data
        assert dealers_data
        assert dealers[0].pk in dealers_data
        assert dealers[1].pk in dealers_data
        assert dealers[2].pk in dealers_data
        assert dealers[3].pk not in dealers_data

        assert dealers_data[dealers[0].pk].get("best_discount")
        assert dealers_data[dealers[1].pk].get("best_discount")
        assert not dealers_data[dealers[2].pk].get("best_discount")

        assert dealers_data[dealers[0].pk]["best_discount"].discount_type == "CD"
        assert dealers_data[dealers[0].pk]["best_discount"].percentage == 5

    @pytest.mark.django_db
    def test_offer_with_characteristics_seller_suitable_marketing_campaigns(
        self, offer_handler_data: dict
    ):
        """
        Checking whether offer handler correctly picks up marketing campaigns for every dealer
        """
        dealers = offer_handler_data["dealers"]
        offer = offer_handler_data["offer_with_characteristic"]
        handler = CustomersOfferHandler(offer, dealers)
        handler._sellers_with_suitable_characteristics()
        handler._sellers_suitable_stock_items_by_characteristics()
        handler._seller_suitable_discounts()
        handler._seller_suitable_marketing_campaigns()

        dealers_data = handler.sellers_data
        assert dealers_data
        assert dealers[0].pk in dealers_data
        assert dealers[1].pk in dealers_data

        assert dealers_data[dealers[0].pk].get("best_marketing_campaign")
        assert dealers_data[dealers[0].pk].get("marketing_campaign_percentage") == 5
        assert dealers_data[dealers[1].pk].get("marketing_campaign_percentage") == 3
        assert not dealers_data[dealers[2].pk].get("marketing_campaign_percentage")

    @pytest.mark.django_db
    def test_offer_with_characteristics_select_best_offer(
        self, offer_handler_data: dict
    ):
        """
        Checking whether offer handler correctly picks up the best offer
        """
        dealers = offer_handler_data["dealers"]
        offer = offer_handler_data["offer_with_characteristic"]
        handler = CustomersOfferHandler(offer, dealers)
        handler._sellers_with_suitable_characteristics()
        handler._sellers_suitable_stock_items_by_characteristics()
        handler._seller_best_stock_item()
        handler._seller_suitable_marketing_campaigns()
        handler._seller_suitable_discounts()
        handler._select_best_offer()

        assert handler.purchase_car == offer_handler_data["choosed_car"]
        assert handler.purchase_seller == offer_handler_data["choosed_dealer"]
        assert handler.purchase_price == 475

    @pytest.mark.django_db
    def test_offer_with_car_suitable_car_on_stock(self, offer_handler_data: dict):
        """
        Checking whether offer handler correctly picks up dealers based on car in offer.
        Here we used car instead of car characteristic as in examples above.
        """
        dealers = offer_handler_data["dealers"]
        offer = offer_handler_data["offer_with_car"]
        handler = CustomersOfferHandler(offer, dealers)
        handler._sellers_with_suitable_car_on_stock()

        assert dealers[0] in handler.sellers
        assert dealers[1] in handler.sellers
        assert dealers[2] in handler.sellers
        assert dealers[3] not in handler.sellers

    @pytest.mark.django_db
    def test_offer_with_car_select_best_offer(self, offer_handler_data: dict):
        """
        Checking whether offer handler correctly select offer.
        Here we used car instead of car characteristic as in examples above.
        """
        dealers = offer_handler_data["dealers"]
        offer = offer_handler_data["offer_with_car"]
        handler = CustomersOfferHandler(offer, dealers)

        handler._sellers_with_suitable_car_on_stock()
        handler._seller_best_stock_item()
        handler._seller_suitable_marketing_campaigns()
        handler._seller_suitable_discounts()
        handler._select_best_offer()

        assert handler.purchase_car == offer_handler_data["choosed_car"]
        assert handler.purchase_seller == offer_handler_data["choosed_dealer"]
        assert handler.purchase_price == 475


@pytest.mark.django_db
def test_task_customer_purchase(offer_handler_data):
    """
    Test task to handle customer offer.
    """
    customer = offer_handler_data["customer"]
    with CaptureQueriesContext(connection) as ctx:
        handle_customer_offer(customer.id)

        q_select, q_update, q_insert, q_len = parse_captured_queries_context(ctx)
        assert q_select <= 12
        assert q_update <= 4
        assert q_insert <= 2
        assert q_len <= 20

    customer.refresh_from_db()

    assert customer.balance == 9525
    assert offer_handler_data["choosed_car"] in customer.cars.all()
