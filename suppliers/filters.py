from common.filters import AmountFilter, CompanyFilter, PricePerOneFilter

from suppliers.models import Supplier, SupplierStockItem


class SupplierFilter(CompanyFilter):
    """
    A filter class for filtering Supplier objects by different options.

    Inherits from CompanyFilter.

    Filters
    -------
    - palce: Filter cars by place(exact match, django-countries choices).
    """

    class Meta:
        model = Supplier
        fields = ["place"]


class SupplierStockFilter(AmountFilter, PricePerOneFilter):
    """
    A filter class for filtering supplier stock objects by different options.

    Inherits from AmountFilter and PricePerOneFilter.

    Filters
    -------
    - amount: Filter stock items by amount (exact match).
    - car: Filter stock items by car id (exact match).
    - price_per_one: Filter stock items by price per one qty (exact match).
    - supplier: Filter supplier stock items by supplier id (exact match).
    """

    class Meta:
        model = SupplierStockItem
        fields = ["amount", "car", "price_per_one", "supplier"]
