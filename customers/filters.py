import django_filters
from common.filters import BalanceFilter

from customers.models import Customer


class CustomerFilter(BalanceFilter):
    """
    A filter class for filtering customers objects by different options.

    Inherits from BalanceFilter.

    Filters
    -------
    - is_active: Filter by active customers (is_active is True).
    - name: Filter customers by their name (exact match).
    - palce: Filter cars by place(exact match, django-countries choices).
    """

    is_active = django_filters.BooleanFilter(
        field_name="is_active", lookup_expr="exact"
    )

    class Meta:
        model = Customer
        fields = ["name", "place"]
