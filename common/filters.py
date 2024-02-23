from django_filters import rest_framework as filters
import django_filters


class PricePerOneFilter(filters.FilterSet):
    """
    A filter class for filtering objects by price.

    Filters
    -------
    - price_per_one__gt: Filter objects with price per one is grater than specified value.
    - price_per_one__lt: Filter objects with price per one is less than specified value.
    """

    price_per_one__gt = django_filters.NumberFilter(
        field_name="price_per_one", lookup_expr="gt"
    )
    price_per_one__lt = django_filters.NumberFilter(
        field_name="price_per_one", lookup_expr="lt"
    )

    class Meta:
        abstract = True


class AmountFilter(filters.FilterSet):
    """
    A filter class for filtering objects by amount.

    Filters
    -------
    - amount__gt: Filter objects with amount is grater than specified value.
    - amount__lt: Filter objects with amount is less than specified value.
    """

    amount__gt = django_filters.NumberFilter(field_name="amount", lookup_expr="gt")
    amount__lt = django_filters.NumberFilter(field_name="amount", lookup_expr="lt")

    class Meta:
        abstract = True


class BalanceFilter(filters.FilterSet):
    """
    A filter class for filtering objects by balance.

    Filters
    -------
    - balance__gt: Filter objects with balance is grater than specified value.
    - balance__lt: Filter objects with balance is less than specified value.
    """

    balance__gt = django_filters.NumberFilter(field_name="balance", lookup_expr="gt")
    balance__lt = django_filters.NumberFilter(field_name="balance", lookup_expr="lt")

    class Meta:
        abstract = True


class CompanyFilter(BalanceFilter):
    """
    A filter class for filtering objects by balance.

    Filters
    -------
    - foundation_date__gt: Filter objects with foundation date is grater than specified value.
    - foundation_date__lt: Filter objects with foundation date is less than specified value.
    """

    foundation_date__gt = django_filters.DateFilter(
        field_name="foundation_date", lookup_expr="gt"
    )
    foundation_date__lt = django_filters.DateFilter(
        field_name="foundation_date", lookup_expr="lt"
    )

    class Meta:
        abstract = True
