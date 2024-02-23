import pytest

from orders.models import (
    CustomerDealsHistory,
    DealerDealsHistory,
)
from orders.services import complete_deal_transaction


@pytest.mark.django_db
class TestTransaction:
    def test_transaction_completed_customer(self, tr_data: dict):
        buyer_customer = tr_data["buyer_customer"]
        seller_dealer = tr_data["seller_dealer"]
        stock_item_dealer = tr_data["stock_item_dealer"]
        car = tr_data["car"]
        price = tr_data["price"]
        amount = tr_data["amount"]
        customer_total_purchases = tr_data["customer_total_purchases"]

        complete_deal_transaction(
            buyer=buyer_customer,
            seller=seller_dealer,
            car=car,
            price=price,
            stock_item=stock_item_dealer,
            amount=amount,
        )

        assert buyer_customer.balance == 1000
        assert seller_dealer.balance == 15000
        assert stock_item_dealer.amount == 9
        customer_total_purchases.refresh_from_db()
        assert customer_total_purchases.amount == 3
        assert car in buyer_customer.cars.all()
        assert CustomerDealsHistory.objects.filter(
            customer=buyer_customer, dealer=seller_dealer, car=car
        ).exists()

    def test_transaction_completed_dealer(self, tr_data: dict):
        buyer_dealer = tr_data["buyer_dealer"]
        seller_supplier = tr_data["seller_supplier"]
        stock_item_supplier = tr_data["stock_item_supplier"]
        car = tr_data["car"]
        price = tr_data["price"]
        dealer_total_purchases = tr_data["dealer_total_purchases"]

        complete_deal_transaction(
            buyer=buyer_dealer,
            seller=seller_supplier,
            car=car,
            price=price,
            stock_item=stock_item_supplier,
            amount=2,
        )

        assert buyer_dealer.balance == 18000
        assert seller_supplier.balance == 82500
        assert stock_item_supplier.amount == 8
        dealer_total_purchases.refresh_from_db()
        assert dealer_total_purchases.amount == 4
        assert buyer_dealer.stock.filter(car__id=car.id).exists()
        assert DealerDealsHistory.objects.filter(
            dealer=buyer_dealer, supplier=seller_supplier, car=car
        )
