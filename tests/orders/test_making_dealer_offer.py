import pytest
from ddf import G

from django.test.utils import CaptureQueriesContext
from django.db import connection

from tests.conftest import parse_captured_queries_context
from cars.models import Car
from dealers.models import Dealer
from orders.tasks import handle_dealer_offer
from suppliers.models import Supplier, SupplierStockItem
from marketing.models import SupplierDiscount, SupplierMarketingCampaign
from orders.models import DealerOffer, TotalSupplierPurchase
from orders.offer_handler import DealerOfferHandler
from suppliers.models import Supplier


@pytest.fixture
def data_for_tests():
    """
    Data for testing offer handler.
    """
    dealer = G(Dealer, balance=10_000)

    car1 = G(Car, brand="Brand1", car_model="Model1", generation="1")
    offer = G(DealerOffer, dealer=dealer, car=car1, amount=1, max_price=1000)
    # offer for bulk discount
    offer_BD = G(DealerOffer, dealer=dealer, car=car1, amount=48, max_price=1000)
    # offer for cumulative discount
    offer_CD = G(DealerOffer, dealer=dealer, car=car1, amount=18, max_price=1000)

    car2 = G(Car, brand="Brand1", car_model="Model1", generation="2")
    car3 = G(Car, brand="Brand3", car_model="Model3", generation="3")

    supplier1 = G(
        Supplier,
        balance=500000,
    )
    supplier1_stock1 = G(
        SupplierStockItem,
        supplier=supplier1,
        car=car1,
        amount=888777,
        price_per_one=500,
    )
    _supplier1_stock2 = G(
        SupplierStockItem, supplier=supplier1, car=car2, amount=99999, price_per_one=600
    )
    _supplier1_stock3 = G(
        SupplierStockItem, supplier=supplier1, car=car3, amount=99999, price_per_one=600
    )
    _supplier1_stock4 = G(
        SupplierStockItem, supplier=supplier1, car=car1, amount=99999, price_per_one=510
    )

    supplier2 = G(Supplier)
    _supplier2_stock1 = G(
        SupplierStockItem, supplier=supplier2, car=car1, amount=99999, price_per_one=490
    )
    _supplier2_stock2 = G(
        SupplierStockItem, supplier=supplier2, car=car2, amount=99999, price_per_one=200
    )
    _supplier2_stock3 = G(
        SupplierStockItem, supplier=supplier2, car=car3, amount=99999, price_per_one=600
    )

    supplier3 = G(Supplier)
    _supplier3_stock1 = G(
        SupplierStockItem, supplier=supplier3, car=car1, amount=99999, price_per_one=501
    )
    _supplier3_stock2 = G(
        SupplierStockItem, supplier=supplier3, car=car2, amount=99999, price_per_one=300
    )
    _supplier3_stock3 = G(
        SupplierStockItem, supplier=supplier3, car=car3, amount=99999, price_per_one=600
    )
    _supplier3_stock4 = G(
        SupplierStockItem, supplier=supplier3, car=car1, amount=99999, price_per_one=505
    )

    supplier4 = G(Supplier)
    _supplier4_stock1 = G(
        SupplierStockItem, supplier=supplier4, car=car3, amount=99999, price_per_one=222
    )

    _supplier1_discount1 = G(
        SupplierDiscount,
        supplier=supplier1,
        discount_type="CD",
        min_amount=9,
        percentage=5,
    )
    _supplier1_discount2 = G(
        SupplierDiscount,
        supplier=supplier1,
        discount_type="BD",
        min_amount=9,
        percentage=5,
    )
    _supplier2_discount = G(
        SupplierDiscount,
        supplier=supplier2,
        discount_type="BD",
        min_amount=40,
        percentage=50,
    )
    _supplier3_discount = G(
        SupplierDiscount,
        supplier=supplier3,
        discount_type="CD",
        min_amount=20,
        percentage=30,
    )

    _total_purchases_supplier1 = G(
        TotalSupplierPurchase, supplier=supplier1, dealer=dealer, amount=10
    )
    _total_purchases_supplier2 = G(
        TotalSupplierPurchase, supplier=supplier2, dealer=dealer, amount=50
    )
    _total_purchases_supplier3 = G(
        TotalSupplierPurchase, supplier=supplier3, dealer=dealer, amount=15
    )

    _supplier1_marketing_campaign1 = G(
        SupplierMarketingCampaign,
        supplier=supplier1,
        percentage=0,
        cars=[car1, car2, car3],
    )
    _supplier1_marketing_campaign2 = G(
        SupplierMarketingCampaign, supplier=supplier1, percentage=5, cars=[car1]
    )
    _supplier2_marketing_campaign1 = G(
        SupplierMarketingCampaign, supplier=supplier2, percentage=3, cars=[car1]
    )
    _supplier3_marketing_campaign1 = G(
        SupplierMarketingCampaign, supplier=supplier3, percentage=5, cars=[car3]
    )
    _supplier4_marketing_campaign1 = G(
        SupplierMarketingCampaign, supplier=supplier4, percentage=55, cars=[car3]
    )

    data = {
        "dealer": dealer,
        "suppliers": [supplier1, supplier2, supplier3, supplier4],
        "offer": offer,
        "offer_BD": offer_BD,
        "offer_CD": offer_CD,
        "choosed_car": car1,
        "choosed_supplier": supplier1,
        "choosed_supplier_BD": supplier2,
        "choosed_supplier_CD": supplier3,
        "supplier1_stock1": supplier1_stock1,
    }
    return data


@pytest.mark.dependency()
@pytest.mark.django_db
def test_dealer_offer_sellers_with_suitable_car_on_stock(data_for_tests):
    """
    Checking whether offer handler correctly picks up suppliers by characteristics
    """
    suppliers = data_for_tests["suppliers"]
    offer = data_for_tests["offer"]
    handler = DealerOfferHandler(offer, suppliers)
    handler._sellers_with_suitable_car_on_stock()
    assert suppliers[0] in handler.sellers
    assert suppliers[1] in handler.sellers
    assert suppliers[2] in handler.sellers
    assert suppliers[3] not in handler.sellers


@pytest.mark.dependency(
    depends=["test_dealer_offer_sellers_with_suitable_car_on_stock"]
)
@pytest.mark.django_db
def test_dealer_offer_seller_best_stock_item(data_for_tests):
    """
    Checking whether offer handler correctly picks up best stock item for every supplier
    """
    suppliers = data_for_tests["suppliers"]
    offer = data_for_tests["offer"]
    handler = DealerOfferHandler(offer, suppliers)
    handler._sellers_with_suitable_car_on_stock()
    handler._seller_best_stock_item()

    sellers_data = handler.sellers_data
    assert sellers_data
    assert suppliers[0].pk in sellers_data

    assert sellers_data[suppliers[0].pk]["best_stock_item"].amount == 888777
    assert sellers_data[suppliers[0].pk]["best_stock_item"].price_per_one == 500


@pytest.mark.dependency(depends=["test_dealer_offer_seller_best_stock_item"])
@pytest.mark.django_db
def test_dealer_offer_seller_suitable_discounts(data_for_tests):
    """
    Checking whether offer handler correctly picks up discounts for every supplier
    """
    suppliers = data_for_tests["suppliers"]
    offer = data_for_tests["offer"]
    handler = DealerOfferHandler(offer, suppliers)
    handler._sellers_with_suitable_car_on_stock()
    handler._seller_best_stock_item()
    handler._seller_suitable_discounts()

    sellers_data = handler.sellers_data
    assert sellers_data
    assert suppliers[0].pk in sellers_data
    assert suppliers[1].pk in sellers_data
    assert suppliers[2].pk in sellers_data
    assert suppliers[3].pk not in sellers_data

    assert sellers_data[suppliers[0].pk].get("best_discount")
    assert not sellers_data[suppliers[2].pk].get("best_discount")

    assert sellers_data[suppliers[0].pk]["best_discount"].discount_type == "CD"
    assert sellers_data[suppliers[0].pk]["best_discount"].percentage == 5


@pytest.mark.dependency(depends=["test_dealer_offer_seller_suitable_discounts"])
@pytest.mark.django_db
def test_dealer_offer_seller_suitable_marketing_campaigns(data_for_tests):
    """
    Checking whether offer handler correctly picks up marketing campaigns for every supplier
    """
    suppliers = data_for_tests["suppliers"]
    offer = data_for_tests["offer"]
    handler = DealerOfferHandler(offer, suppliers)
    handler._sellers_with_suitable_car_on_stock()
    handler._seller_best_stock_item()
    handler._seller_suitable_discounts()
    handler._seller_suitable_marketing_campaigns()

    sellers_data = handler.sellers_data
    assert sellers_data
    assert suppliers[0].pk in sellers_data
    assert suppliers[1].pk in sellers_data

    assert sellers_data[suppliers[0].pk].get("best_marketing_campaign")
    assert sellers_data[suppliers[0].pk].get("marketing_campaign_percentage") == 5
    assert sellers_data[suppliers[1].pk].get("marketing_campaign_percentage") == 3
    assert not sellers_data[suppliers[2].pk].get("marketing_campaign_percentage")


@pytest.mark.dependency(
    depends=["test_dealer_offer_seller_suitable_marketing_campaigns"]
)
@pytest.mark.django_db
def test_dealer_offer_analyze_perspective_cooperation_cumulative_discount(
    data_for_tests,
):
    """
    Checking whether offer handler correctly picks up marketing campaigns for every supplier
    test MAY BE FAILED after changing weights.
    """
    suppliers = data_for_tests["suppliers"]
    offer = data_for_tests["offer_CD"]
    handler = DealerOfferHandler(offer, suppliers)
    handler._sellers_with_suitable_car_on_stock()
    handler._seller_best_stock_item()
    handler._seller_suitable_discounts()
    handler._seller_suitable_marketing_campaigns()
    handler._select_best_offer()
    handler._analyze_perspective_cooperation()

    assert (
        handler.forecast_cooperation_with_supplier
        == data_for_tests["choosed_supplier_CD"]
    )


@pytest.mark.django_db
def test_task_dealer_purchase(data_for_tests):
    """
    Test task to handle customer offer.
    """
    dealer = data_for_tests["dealer"]
    with CaptureQueriesContext(connection) as ctx:
        handle_dealer_offer(dealer.id)

        q_select, q_update, q_insert, q_len = parse_captured_queries_context(ctx)
        assert q_select <= 13
        assert q_update <= 4
        assert q_insert <= 2
        assert q_len <= 23

    dealer.refresh_from_db()

    assert dealer.balance == 1450
    assert any(item.car == data_for_tests["choosed_car"] for item in dealer.stock.all())
