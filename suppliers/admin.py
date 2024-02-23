from django.contrib import admin

from common.admin import BalanceFilter, BaseAdmin
from suppliers.models import Supplier, SupplierStockItem


@admin.register(Supplier)
class SupplierAdmin(BaseAdmin):
    """
    Admin class for Supplier model.
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


@admin.register(SupplierStockItem)
class SupplierStockItemAdmin(BaseAdmin):
    """
    Admin class for SupplierStockItem model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "car",
        "amount",
        "price_per_one",
        "supplier",
    ] + BaseAdmin.list_display
    list_filter = ["car__brand"] + BaseAdmin.list_filter
    search_fields = ["car__brand", "car__car_model", "car__generation"]
