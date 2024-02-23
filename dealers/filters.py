from common.filters import AmountFilter, CompanyFilter, PricePerOneFilter
from dealers.models import Dealer, DealerStockItem


class DealerFilter(CompanyFilter):
    """
    A filter class for filtering Dealer objects by different options.

    Inherits from CompanyFilter.

    Filters
    -------
    - palce: Filter cars by place(exact match, django-countries choices).
    """

    class Meta:
        model = Dealer
        fields = ["place"]


class DealerStockFilter(AmountFilter, PricePerOneFilter):
    """
    A filter class for filtering dealer stock objects by different options.

    Inherits from AmountFilter and PricePerOneFilter

    Filters
    -------
    - amount: Filter cars by amount (exact match).
    - car: Filter cars by car id (exact match).
    - price_per_one: Filter cars by price per one qty (exact match).
    """

    class Meta:
        model = DealerStockItem
        fields = ["amount", "car", "price_per_one"]
