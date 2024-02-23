from typing import Any
from django.contrib import admin
from django.db.models import QuerySet

from car_dealership.settings import ADMIN_PANEL_PAGINATION


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin model.

    Methods:
        set_inactive_entries: A custom action to make objects inactive.
    """

    list_display = ["is_active", "updated_at", "created_at"]
    list_filter = ["is_active", "updated_at", "created_at"]
    search_fields = ["pk"]
    date_hierarchy = "created_at"
    list_per_page = ADMIN_PANEL_PAGINATION
    actions = ["set_inactive_entries"]

    @admin.action(description="make inactive")
    def set_inactive_entries(self, request, qs: QuerySet):
        """
        Admin action.

        Makes all entries inactive (is_active = False).
        """
        inactive_counter = qs.update(is_active=False)
        self.message_user(request, f"{inactive_counter} entries were updated")


class BalanceFilter(admin.SimpleListFilter):
    """
    Filter class for balance field
    """

    title = "Balance"
    parameter_name = "balance_filter"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return (
            ("0", "0"),
            ("0_to_1k", "from 0 to 1k"),
            ("10k_to_100k", "from 10k to 100k"),
            ("100k", "100k +"),
        )

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.filter(balance__exact=0)
        elif self.value() == "0_to_1k":
            return queryset.filter(balance__gt=0, balance__lte=10000)
        elif self.value() == "10k_to_100k":
            return queryset.filter(balance__gt=10000, balance__lte=100000)
        elif self.value() == "100k":
            return queryset.filter(balance__gt=100000)
        else:
            return queryset
