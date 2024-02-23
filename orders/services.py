from typing import List, Dict, Union
from django.db import transaction
from django.conf import settings

from orders.models import (
    CustomerDealsHistory,
    CustomerOffer,
    DealerDealsHistory,
    DealerOffer,
)
from orders.offer_handler import CustomersOfferHandler, DealerOfferHandler
from dealers.models import Dealer, DealerStockItem
from cars.models import Car, CarStockItem
from suppliers.models import Supplier
from customers.models import Customer
from common.models import Company
from orders.utils import (
    check_average_day_sellings,
    count_item_per_purchase,
    forecast_sellings,
    sort_stock_data,
)

StockItemType = Dict[str, Union[DealerStockItem, int, int]]


def dealer_regular_purchase_handler(dealer: Dealer, suppliers: List[Supplier]):
    """
    Function to handle cars purchase on dealer's stock.

    Checks deals history for every stock item and calculate amount of cars to buy.
    Then it searchs for best suppliers' offers and completes it.
    """
    stock_data: List[StockItemType] = prepare_stock_data(dealer)
    stock_data = sort_stock_data(stock_data, "total")
    for item in stock_data:
        offer = DealerOffer(
            dealer=dealer, car=item["stock_item"].car, amount=item["amount_to_buy"]
        )
        offer_handler = DealerOfferHandler(offer, suppliers)
        offer_handler.process_offer()

        if not offer_handler.purchase_seller:
            continue
        if dealer.balance >= offer_handler.purchase_price * item["amount_to_buy"]:
            complete_deal_transaction(
                buyer=dealer,
                seller=offer_handler.purchase_seller,
                car=offer_handler.purchase_car,
                price=offer_handler.purchase_price,
                stock_item=offer_handler.purchase_stock_item,
                amount=item["amount_to_buy"],
            )
        elif (
            offer_handler.purchase_discount
            and offer_handler.purchase_discount.discount_type != "BD"
        ):
            amount = dealer.balance // offer_handler.purchase_price
            if amount > 0:
                complete_deal_transaction(
                    buyer=dealer,
                    seller=offer_handler.purchase_seller,
                    car=offer_handler.purchase_car,
                    price=offer_handler.purchase_price,
                    stock_item=offer_handler.purchase_stock_item,
                    amount=amount,
                )
                continue
            break
        else:
            break


def prepare_stock_data(dealer) -> List[StockItemType]:
    """
    Function to prepare stock items data to future handling.

    Returns list of dicts. Every dict in list represents necessary data for each stock item.
    Constist of stock item, amount to buy on stock and total amount of sellings of specific car for last three months.
    """
    stock_data = []
    for stock_item in dealer.stock.all():
        total, average = check_average_day_sellings(
            stock_item, dealer.three_month_history
        )
        days = forecast_sellings(stock_item, average)
        if days < settings.SELL_OUT_DAYS:
            amount_to_buy = count_item_per_purchase(average, days)
            if amount_to_buy == 0:
                continue

            stock_data.append(
                {
                    "stock_item": stock_item,
                    "amount_to_buy": amount_to_buy,
                    "total": total,
                }
            )
    return stock_data


def complete_deal_transaction(
    buyer,
    seller: Company,
    car: Car,
    price: int,
    stock_item: CarStockItem,
    amount: int = 1,
):
    """
    Function to make a transaction to buy car for dealer or customer.

    Changes all data related for transaction or rollback it if some error was catched during this transaction.
    """
    with transaction.atomic():
        total_sum = int(price * amount)

        buyer.balance -= total_sum
        buyer.save()

        seller.balance += total_sum
        seller.save()

        stock_item.amount -= amount
        stock_item.save()

        if isinstance(buyer, Customer):
            total_purchase, created = seller.total_purchases.get_or_create(
                customer=buyer, dealer=seller, defaults={"amount": amount}
            )
            if not created:
                total_purchase.add_amount(amount)

            buyer.cars.add(car)
            CustomerDealsHistory.objects.create(
                customer=buyer,
                dealer=seller,
                car=car,
                amount=amount,
                price_per_one=price,
            )
        elif isinstance(buyer, Dealer):
            total_purchase, created = seller.total_purchases.get_or_create(
                dealer=buyer, supplier=seller, defaults={"amount": amount}
            )
            if not created:
                total_purchase.add_amount(amount)

            stock_item, created = buyer.stock.get_or_create(
                dealer=buyer,
                car=car,
                defaults={"amount": amount, "price_per_one": price},
            )

            if not created:
                stock_item.add_amount(amount)

            DealerDealsHistory.objects.create(
                dealer=buyer,
                supplier=seller,
                car=car,
                amount=amount,
                price_per_one=price,
            )


def customer_purchase_handler(offer):
    dealers_queryset = Dealer.objects.prepare_for_offer()
    offer_handler = CustomersOfferHandler(offer=offer, dealers=dealers_queryset)
    offer_handler.process_offer()

    if (
        offer_handler.purchase_seller
        and offer.customer.balance >= offer_handler.purchase_price
    ):
        complete_deal_transaction(
            buyer=offer.customer,
            seller=offer_handler.purchase_seller,
            car=offer_handler.purchase_car,
            price=offer_handler.purchase_price,
            stock_item=offer_handler.purchase_stock_item,
            amount=1,
        )


def dealer_purchase_handler(offer):
    suppliers_queryset = Supplier.objects.pre_order_queryset()
    offer_handler = DealerOfferHandler(offer=offer, suppliers=suppliers_queryset)
    offer_handler.process_offer()

    if (
        offer_handler.purchase_seller
        and offer.dealer.balance >= offer_handler.purchase_price * offer.amount
    ):
        complete_deal_transaction(
            buyer=offer.dealer,
            seller=offer_handler.purchase_seller,
            car=offer_handler.purchase_car,
            price=offer_handler.purchase_price,
            stock_item=offer_handler.purchase_stock_item,
            amount=offer.amount,
        )


def customer_regular_purchase_handler(
    customer: Customer, dealers: List[Dealer], car_id: int, max_price: int
):
    """
    Function to create and handle customer offer with random car.

    Choose car for offer, then create offer and searches for best dealers' offers and completes it.
    """
    car = Car.objects.get(pk=car_id)
    offer = CustomerOffer(customer=customer, max_price=max_price, car=car)

    offer_handler = CustomersOfferHandler(offer, dealers)
    offer_handler.process_offer()
    if (
        offer_handler.purchase_seller
        and offer.customer.balance >= offer_handler.purchase_price
    ):
        complete_deal_transaction(
            buyer=offer.customer,
            seller=offer_handler.purchase_seller,
            car=offer_handler.purchase_car,
            price=offer_handler.purchase_price,
            stock_item=offer_handler.purchase_stock_item,
            amount=1,
        )


def handle_cooperation_profitability(dealer: Dealer, suppliers: List[Supplier]):
    """
    Function to update dealer's list of suppliers with the most profitable values.

    Searches for best supplier for every stock item.
    """
    new_suppliers = []
    for stock_item in dealer.stock.all():
        offer = DealerOffer(dealer=dealer, car=stock_item.car, amount=1)
        offer_handler = DealerOfferHandler(offer, suppliers)
        offer_handler.process_offer()
        if offer_handler.purchase_seller:
            new_suppliers.append(offer_handler.purchase_seller)

    if new_suppliers:
        dealer.suppliers.clear()

        dealer.suppliers.set(new_suppliers)
