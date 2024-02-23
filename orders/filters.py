import django_filters
from common.filters import AmountFilter, PricePerOneFilter

from orders.models import (
    CustomerDealsHistory,
    DealerDealsHistory,
    TotalDealerPurchase,
    TotalSupplierPurchase,
)


class DealsHistoryFilter(AmountFilter, PricePerOneFilter):
    """
    An abstract filter class for filtering delas history objects by different options.

    Inherits from AmountFilter and PricePerOneFilter.

    Filters
    -------
    - date__gt: Filter user profile with date is grater than specified value.
    - date__lt: Filter user profile with date year is less than specified value.
    """

    date__gt = django_filters.DateFilter(field_name="date", lookup_expr="gt")
    date__lt = django_filters.DateFilter(field_name="date", lookup_expr="lt")

    class Meta:
        abstract = True


class CustomerDealsHistoryFilter(DealsHistoryFilter):
    """
    A filter class for filtering customers delas history objects.

    Inherits from DealsHistoryFilter.

    Filters
    -------
    - cars: Filter customers deals history by cars's id (exact match).
    - dealer: Filter customers deals history by dealer's id (exact match).
    """

    class Meta:
        model = CustomerDealsHistory
        fields = ["car", "dealer"]


class DealerDealsWithCustomerFilter(DealsHistoryFilter):
    """
    A filter class for filtering dealers delas history with customers.

    Inherits from DealsHistoryFilter.

    Filters
    -------
    - car: Filter dealers deals history by cars's id (exact match).
    - customer: Filter dealers deals history by customer's id (exact match).
    """

    class Meta:
        model = CustomerDealsHistory
        fields = ["car", "customer"]


class DealerDealsWithSupplierFilter(DealsHistoryFilter):
    """
    A filter class for filtering dealers delas history with supppliers.

    Inherits from DealsHistoryFilter.

    Filters
    -------
    - cars: Filter dealers deals history by cars's id (exact match).
    - supplier: Filter dealers deals history by suppliers's id (exact match).
    """

    class Meta:
        model = DealerDealsHistory
        fields = ["car", "supplier"]


class DealerTotalDealsWithCustomerFilter(AmountFilter):
    """
    A filter class for filtering dealers total delas history with customers.

    Inherits from AmountFilter.

    Filters
    -------
    - customer: Filter dealers total deals history by customer's id (exact match).
    """

    class Meta:
        model = TotalDealerPurchase
        fields = ["customer"]


class DealerTotalDealsWithSupplierFilter(AmountFilter):
    """
    A filter class for filtering dealers total delas history with suppliers.

    Inherits from AmountFilter.

    Filters
    -------
    - supplier: Filter dealers total deals history by supplier's id (exact match).
    """

    class Meta:
        model = TotalSupplierPurchase
        fields = ["supplier"]


class SupplierDealsWithDealerFilter(DealsHistoryFilter):
    """
    A filter class for filtering suppliers delas history with dealers.

    Inherits from DealsHistoryFilter.

    Filters
    -------
    - car: Filter suppliers deals history by cars's id (exact match).
    - dealer: Filter suppliers deals history by dealer's id (exact match).
    """

    class Meta:
        model = DealerDealsHistory
        fields = ["car", "dealer"]


class SupplierTotalDealsWithDealerFilter(AmountFilter):
    """
    A filter class for filtering suppliers total delas history with dealers.

    Inherits from AmountFilter.

    Filters
    -------
    - dealer: Filter supplier total deals history by dealer's id (exact match).
    """

    class Meta:
        model = TotalSupplierPurchase
        fields = ["dealer"]
