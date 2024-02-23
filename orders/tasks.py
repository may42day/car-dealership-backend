from celery import shared_task
from random import choice

from car_dealership.celery import app as celery_app
from customers.models import Customer
from orders.services import (
    customer_purchase_handler,
    customer_regular_purchase_handler,
    dealer_purchase_handler,
    dealer_regular_purchase_handler,
    handle_cooperation_profitability,
)
from orders.models import CustomerOffer, DealerOffer
from suppliers.models import Supplier
from dealers.models import Dealer, DealerStockItem
from users.models import UserProfile


@celery_app.task
def handle_customer_offer(customer_id: int):
    """
    Task to handle customer's offer.
    """
    offer = CustomerOffer.objects.prepare_offer(customer_id).last()
    if offer:
        customer_purchase_handler(offer)


@celery_app.task
def handle_dealer_offer(dealer_id: int):
    """
    Task to handle dealer's offer.
    """
    offer = DealerOffer.objects.prepare_offer(dealer_id).last()
    if offer:
        dealer_purchase_handler(offer)


@celery_app.task
def run_cars_purchase(dealer_id: int):
    """
    Task to start cars purchase on dealer's stock.
    """
    suppliers_queryset = Supplier.objects.pre_order_queryset()
    dealer_queryset = Dealer.objects.pre_order_queryset(dealer_id).first()
    dealer_regular_purchase_handler(dealer_queryset, suppliers_queryset)


@celery_app.task
def run_customer_purchase_with_random_car(
    customer_id: int, random_car_pk: int, max_price: int
):
    """
    Task to make and process customer offer with random car.
    """
    customer_queryset = Customer.objects.pre_offer_queryset(customer_id).first()
    dealers_queryset = Dealer.objects.pre_customer_order_queryset()
    customer_regular_purchase_handler(
        customer_queryset, dealers_queryset, random_car_pk, max_price
    )


@celery_app.task
def check_cooperation_profitability(dealer_id: int):
    """
    Task to check dealers' cooperation with suppliers.
    """
    dealer = Dealer.objects.pre_order_queryset(dealer_id).first()
    suppliers_queryset = Supplier.objects.pre_order_queryset()
    if dealer:
        handle_cooperation_profitability(dealer, suppliers_queryset)


@shared_task
def regular_order_on_dealer_stock():
    """
    Task to make orders on stock for every active dealer with positive balance.
    """
    for dealer in Dealer.objects.active():
        if dealer.user_profile and dealer.balance > 0:
            run_cars_purchase.delay(dealer.id)


@shared_task
def regular_order_by_customers():
    """
    Task to make orders by customers for every active customer with positive balance.
    """
    stock_items = DealerStockItem.objects.all()
    for customer in Customer.objects.active():
        if Customer.user_profile and customer.balance > 0:
            random_stock_item = choice(stock_items)
            random_car_pk = random_stock_item.car.pk
            max_price = random_stock_item.price_per_one
            run_customer_purchase_with_random_car.delay(
                customer.id, random_car_pk, max_price
            )


@shared_task
def regular_cooperation_profitability_check():
    """
    Task to check dealers' cooperation with suppliers.
    """
    for dealer in Dealer.objects.active():
        check_cooperation_profitability(dealer.pk)
