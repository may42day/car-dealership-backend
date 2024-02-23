import json
import os
from typing import Any

from django.core.management.base import BaseCommand
from car_dealership import settings

from cars.models import Car, CarCharacteristic
from customers.models import Customer
from suppliers.models import Supplier, SupplierStockItem
from dealers.models import Dealer, DealerStockItem
from marketing.models import (
    SupplierDiscount,
    SupplierMarketingCampaign,
    DealerDiscount,
    DealerMarketingCampaign,
)
from orders.models import (
    CustomerOffer,
    CustomerDealsHistory,
    DealerDealsHistory,
    TotalDealerPurchase,
    TotalSupplierPurchase,
)
from users.models import UserProfile


def error_handler(func):
    def wrapper(*args, **kwargs):
        _self, file_name, model = args
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error during handling {file_name}, model {model}.Error: {e}")

    return wrapper


class Command(BaseCommand):
    help = "Creating database entries"

    def handle(self, *args, **kwargs):
        self._create_from_json("cars.json", Car)
        # self._create_from_json("cars_characteristics.json", CarCharacteristic)
        self._create_users("users.json", UserProfile)
        # self._create_from_json("customers.json", Customer)
        # self._add_customers_cars("customers_cars.json", Customer)
        # self._create_from_json("dealers.json", Dealer)
        # self._add_dealers_cars_characteristics(
        #     "dealers_cars_characteristics.json", Dealer
        # )
        # self._create_from_json("suppliers.json", Supplier)
        # self._add_dealers_suppliers("dealers_suppliers.json", Dealer)
        # self._add_dealers_customers("dealers_customers.json", Dealer)
        self._create_from_json("suppliers_stock.json", SupplierStockItem)
        self._create_from_json("dealers_stock.json", DealerStockItem)
        self._create_from_json("suppliers_discounts.json", SupplierDiscount)
        self._create_from_json("dealers_discounts.json", DealerDiscount)
        self._create_from_json("suppliers_marketing.json", SupplierMarketingCampaign)
        self._add_suppliers_cars_for_marketing(
            "suppliers_cars_for_marketing.json", SupplierMarketingCampaign
        )
        self._create_from_json("dealer_marketing.json", DealerMarketingCampaign)
        self._add_dealers_cars_for_marketing(
            "dealers_cars_for_marketing.json", DealerMarketingCampaign
        )
        # self._create_from_json("customer_offers.json", CustomerOffer)
        # self._create_from_json("customers_deals_history.json", CustomerDealsHistory)
        # self._create_from_json("dealers_deals_history.json", DealerDealsHistory)
        # self._create_from_json("total_dealer_purchases.json", TotalDealerPurchase)
        # self._create_from_json("total_supplier_purchases.json", TotalSupplierPurchase)

    def _get_file_path(self, file_name):
        return os.path.join(settings.BASE_DIR, "commands_manager", "db_data", file_name)

    def _get_data_from_file(self, file_name):
        file_path = self._get_file_path(file_name)
        with open(file_path) as json_file:
            return json.load(json_file)

    @error_handler
    def _create_from_json(self, file_name, model):
        data = self._get_data_from_file(file_name)
        for instance_data in data["data"]:
            model.objects.create(**instance_data)
        print(f"{model.__name__}: success")

    @error_handler
    def _add_customers_cars(self, file_name, model):
        data = self._get_data_from_file(file_name)
        for instance in data["data"]:
            customer_id = instance["id"]
            car_id = instance["car_id"]

            customer = model.objects.get(pk=customer_id)
            car = Car.objects.get(pk=car_id)
            customer.cars.add(car)
        print(f"{model.__name__}: success")

    @error_handler
    def _add_dealers_cars_characteristics(self, file_name, model):
        data = self._get_data_from_file(file_name)
        for instance in data["data"]:
            dealer_id = instance["id"]
            characteristic_id = instance["characteristic_id"]

            dealer = model.objects.get(pk=dealer_id)
            characteristic = CarCharacteristic.objects.get(pk=characteristic_id)
            dealer.car_characteristics.add(characteristic)

        print(f"{model.__name__}: success")

    @error_handler
    def _add_dealers_suppliers(self, file_name, model):
        data = self._get_data_from_file(file_name)
        for instance in data["data"]:
            dealer_id = instance["id"]
            supplier_id = instance["supplier_id"]

            dealer = model.objects.get(pk=dealer_id)
            supplier = Supplier.objects.get(pk=supplier_id)
            dealer.suppliers.add(supplier)
        print(f"{model.__name__}: success")

    @error_handler
    def _add_dealers_customers(self, file_name, model):
        data = self._get_data_from_file(file_name)
        for instance in data["data"]:
            dealer_id = instance["id"]
            customer_id = instance["customer_id"]

            dealer = model.objects.get(pk=dealer_id)
            customer = Customer.objects.get(pk=customer_id)
            dealer.customers.add(customer)

        print(f"{model.__name__}: success")

    @error_handler
    def _add_dealers_cars_for_marketing(self, file_name, model):
        data = self._get_data_from_file(file_name)
        for instance in data["data"]:
            marketing_id = instance["id"]
            car_id = instance["car_id"]

            marketing = model.objects.get(pk=marketing_id)
            car = Car.objects.get(pk=car_id)
            marketing.cars.add(car)

        print(f"{model.__name__}: success")

    @error_handler
    def _add_suppliers_cars_for_marketing(self, file_name, model):
        data = self._get_data_from_file(file_name)
        for instance in data["data"]:
            marketing_id = instance["id"]
            car_id = instance["car_id"]

            marketing = model.objects.get(pk=marketing_id)
            car = Car.objects.get(pk=car_id)
            marketing.cars.add(car)

        print(f"{model.__name__}: success")

    @error_handler
    def _create_users(self, file_name, model):
        users_profiles = self._get_data_from_file(file_name)
        dealers = iter(self._get_data_from_file("dealers.json")["data"])
        suppliers = iter(self._get_data_from_file("suppliers.json")["data"])
        customers = iter(self._get_data_from_file("customers.json")["data"])

        for instance in users_profiles["data"]:

            user = model.objects.create(**instance)
            if user.role == UserProfile.CUSTOMER:
                Customer.objects.filter(user_profile=user).update(**next(customers))
            elif user.role == UserProfile.DEALER:
                Dealer.objects.filter(user_profile=user).update(**next(dealers))
            else:
                Supplier.objects.filter(user_profile=user).update(**next(suppliers))

            password = instance.get("password")
            if password:
                user.set_password(password)
                user.save()

        print(f"UserProfile, Customer, Dealer, Supplier success")
