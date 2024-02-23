from django.contrib import admin

from common.admin import BalanceFilter, BaseAdmin
from dealers.models import (
    Dealer,
    DealerStockItem,
)


@admin.register(Dealer)
class DealerAdmin(BaseAdmin):
    """
    Admin class for Dealer model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "name",
        "balance",
        "place",
        "foundation_date",
    ] + BaseAdmin.list_display
    list_filter = [BalanceFilter] + BaseAdmin.list_filter
    search_fields = ["name"]
    list_editable = ["balance"]


@admin.register(DealerStockItem)
class DealerStockItemAdmin(BaseAdmin):
    """
    Admin class for DealerStockItem model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = ["car", "amount", "price_per_one", "dealer"] + BaseAdmin.list_display
    list_filter = ["car__brand"] + BaseAdmin.list_filter
    search_fields = ["car__brand", "car__car_model", "car__generation"]
