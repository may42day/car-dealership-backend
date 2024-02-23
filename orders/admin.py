from django.contrib import admin

from common.admin import BaseAdmin
from orders.models import (
    CustomerOffer,
    CustomerDealsHistory,
    DealerDealsHistory,
    TotalDealerPurchase,
    TotalSupplierPurchase,
)


@admin.register(CustomerOffer)
class CustomerOfferAdmin(BaseAdmin):
    """
    Admin class for CustomerOffer model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "customer",
        "car",
        "max_price",
        "is_closed",
        "bought_car",
        "car_price",
    ] + BaseAdmin.list_display
    list_filter = ["is_closed"] + BaseAdmin.list_filter


@admin.register(CustomerDealsHistory)
class CustomerDealsHistoryAdmin(BaseAdmin):
    """
    Admin class for CustomerDealsHistory model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "car",
        "amount",
        "price_per_one",
        "customer",
        "dealer",
        "date",
    ] + BaseAdmin.list_display
    list_filter = ["date"] + BaseAdmin.list_filter


@admin.register(DealerDealsHistory)
class DealerDealsHistoryAdmin(BaseAdmin):
    """
    Admin class for DealerDealsHistory model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "car",
        "amount",
        "price_per_one",
        "dealer",
        "supplier",
        "date",
    ] + BaseAdmin.list_display
    list_filter = ["date"] + BaseAdmin.list_filter


@admin.register(TotalDealerPurchase)
class TotalDealerPurchaseAdmin(BaseAdmin):
    """
    Admin class for TotalDealerPurchase model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = ["amount", "dealer", "customer"] + BaseAdmin.list_display


@admin.register(TotalSupplierPurchase)
class TotalSupplierPurchaseAdmin(BaseAdmin):
    """
    Admin class for TotalSupplierPurchase model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = ["amount", "dealer", "supplier"] + BaseAdmin.list_display
