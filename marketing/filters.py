from django_filters import rest_framework as filters
import django_filters

from marketing.models import (
    DealerDiscount,
    DealerMarketingCampaign,
    Discount,
    SupplierDiscount,
    SupplierMarketingCampaign,
)


class PercentageFilter(filters.FilterSet):
    """
    An abstract filter class for filtering objects by percentage field.

    Filters
    -------
    - percentage__gt: Filter objects with percentage is grater than specified value.
    - percentage__lt: Filter objects with percentage is less than specified value.
    """

    percentage__gt = django_filters.NumberFilter(
        field_name="percentage", lookup_expr="gt"
    )
    percentage__lt = django_filters.NumberFilter(
        field_name="percentage", lookup_expr="lt"
    )

    class Meta:
        abstract = True


class MarketingCampaignFilter(PercentageFilter):
    """
    An abstract filter class for filtering marketing campaign objects by different options.

    Inherits from PercentageFilter.

    Filters
    -------
    - start_date__gt: Filter objects with start date is grater than specified value.
    - start_date__lt: Filter objects with start date is less than specified value.
    - end_date__gt: Filter objects with end date is grater than specified value.
    - end_date__lt: Filter objects with end date is less than specified value.
    """

    start_date__gt = django_filters.DateFilter(
        field_name="start_date", lookup_expr="gt"
    )
    start_date__lt = django_filters.DateFilter(
        field_name="start_date", lookup_expr="lt"
    )
    end_date__gt = django_filters.DateFilter(field_name="end_date", lookup_expr="gt")
    end_date__lt = django_filters.DateFilter(field_name="end_date", lookup_expr="lt")

    class Meta:
        abstract = True


class DealerMarketingCampaignFilter(MarketingCampaignFilter):
    """
    An filter class for filtering dealer marketing campaign objects.

    Inherits from MarketingCampaignFilter.

    Filters
    -------
    - dealer: Filter marketing campaigns by dealer's id (exact match).
    - cars: Filter marketing campaigns by cars's id (exact match).
    """

    class Meta:
        model = DealerMarketingCampaign
        fields = ["dealer", "cars"]


class SupplierMarketingCampaignFilter(MarketingCampaignFilter):
    """
    An filter class for filtering supplier marketing campaign objects.

    Inherits from MarketingCampaignFilter.

    Filters
    -------
    - supplier: Filter marketing campaigns by supplier's id (exact match).
    - cars: Filter marketing campaigns by cars's id (exact match).
    """

    class Meta:
        model = SupplierMarketingCampaign
        fields = ["supplier", "cars"]


class DiscountFilter(PercentageFilter):
    """
    An abstract filter class for filtering discounts objects by different options.

    Inherits from PercentageFilter.

    Filters
    -------
    - min_amount__gt: Filter objects with min_amount is grater than specified value.
    - min_amount__lt: Filter objects with min_amount is less than specified value.
    - discount_type: Filter objects by discount type (choices=Discount.DISCOUNT_TYPE_CHOICES).
    """

    min_amount__gt = django_filters.NumberFilter(
        field_name="min_amount", lookup_expr="gt"
    )
    min_amount__lt = django_filters.NumberFilter(
        field_name="min_amount", lookup_expr="lt"
    )
    discount_type = django_filters.ChoiceFilter(
        field_name="discount_type",
        choices=Discount.DISCOUNT_TYPE_CHOICES,
    )


class DealerDiscountFilter(DiscountFilter):
    """
    An filter class for filtering dealer discounts objects.

    Inherits from DiscountFilter.

    Filters
    -------
    - dealer: Filter discounts by dealers' id.
    - discount_type: Filter objects by discount type (choices=Discount.DISCOUNT_TYPE_CHOICES).
    """

    class Meta:
        model = DealerDiscount
        fields = ["discount_type", "dealer"]


class SupplierDiscountFilter(DiscountFilter):
    """
    An filter class for filtering supplier discounts objects.

    Inherits from DiscountFilter.

    Filters
    -------
    - supplier: Filter discounts by suppliers' id.
    - discount_type: Filter objects by discount type (choices=Discount.DISCOUNT_TYPE_CHOICES).
    """

    class Meta:
        model = SupplierDiscount
        fields = ["discount_type", "supplier"]
