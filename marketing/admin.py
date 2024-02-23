from django.contrib import admin

from common.admin import BaseAdmin
from marketing.models import (
    DealerDiscount,
    SupplierDiscount,
    DealerMarketingCampaign,
    SupplierMarketingCampaign,
)


@admin.register(DealerDiscount)
class DealerDiscountAdmin(BaseAdmin):
    """
    Admin class for DealerDiscount model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "name",
        "min_amount",
        "discount_type",
        "dealer",
    ] + BaseAdmin.list_display
    list_filter = ["discount_type", "min_amount"] + BaseAdmin.list_filter
    search_fields = ["name"]


@admin.register(SupplierDiscount)
class SupplierDiscountAdmin(BaseAdmin):
    """
    Admin class for SupplierDiscount model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "name",
        "min_amount",
        "discount_type",
        "supplier",
    ] + BaseAdmin.list_display
    list_filter = ["discount_type", "min_amount"] + BaseAdmin.list_filter
    search_fields = ["name"]


@admin.register(DealerMarketingCampaign)
class DealerMarketingCampaignAdmin(BaseAdmin):
    """
    Admin class for DealerMarketingCampaign model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "name",
        "description",
        "start_date",
        "end_date",
        "dealer",
    ] + BaseAdmin.list_display
    list_filter = ["start_date", "end_date"] + BaseAdmin.list_filter
    search_fields = ["name"]


@admin.register(SupplierMarketingCampaign)
class SupplierMarketingCampaignAdmin(BaseAdmin):
    """
    Admin class for SupplierMarketingCampaign model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "name",
        "description",
        "start_date",
        "end_date",
        "supplier",
    ] + BaseAdmin.list_display
    list_filter = ["start_date", "end_date"] + BaseAdmin.list_filter
    search_fields = ["name"]
