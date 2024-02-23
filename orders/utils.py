from typing import Dict, Union, List

from django.conf import settings
from django.utils import timezone

from cars.models import CarStockItem
from dealers.models import DealerStockItem
from orders.models import DealHistory


def forecast_sellings(stock_item: CarStockItem, average: int):
    """
    Function to forecast sellings of specific stock item based on average sellings per day.
    """
    return 0 if not average else int(stock_item.amount / average)


def check_average_day_sellings(
    stock_item: CarStockItem,
    history: List[DealHistory],
) -> (int, int):
    """
    Function to get total and average amount of selling of specific car.
    """

    related_deals = [deal for deal in history if deal.car == stock_item.car]
    total = len(related_deals)
    if total:
        first_date = min([deal.date for deal in related_deals])
        now = timezone.now()
        days = max(1, (now - first_date).days)
        return total, int(total / days)
    return 0, 0


def count_item_per_purchase(average: int, days: int) -> int:
    """
    Function to calculate amount for new cars purchase based on set up days for selling and delivery.
    """
    total_days = settings.SELL_OUT_DAYS + (settings.AVERAGE_DELIVERY_DAYS - days)

    return total_days * average


def sort_stock_data(
    stock_data: List[Dict[str, Union[DealerStockItem, int, int]]], key
) -> list:
    """
    Function to sort list of dics of stock data by specific key.
    """
    return sorted(stock_data, key=lambda k: k[key], reverse=True)
