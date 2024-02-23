from django.contrib import admin

from common.admin import BalanceFilter, BaseAdmin
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    """
    Admin class for Customer model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = ["name", "balance", "place"] + BaseAdmin.list_display
    list_filter = [BalanceFilter] + BaseAdmin.list_filter
    search_fields = ["name"]
    list_editable = ["balance"]
