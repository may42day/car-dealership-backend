from django.contrib import admin

from cars.models import Car, CarCharacteristic
from common.admin import BaseAdmin


@admin.register(Car)
class CarAdmin(BaseAdmin):
    """
    Admin class for Car model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "brand",
        "car_model",
        "generation",
        "year_release",
        "year_end_of_production",
    ] + BaseAdmin.list_display
    list_filter = ["brand"] + BaseAdmin.list_filter
    search_fields = ["brand", "car_model"]


@admin.register(CarCharacteristic)
class CarCharacteristicAdmin(BaseAdmin):
    """
    Admin class for CarCharacteristic model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = [
        "brand",
        "car_model",
        "generation",
        "year_release",
        "year_end_of_production",
    ] + BaseAdmin.list_display
    list_filter = ["brand", "car_model"] + BaseAdmin.list_filter
    search_fields = ["brand", "car_model"]
