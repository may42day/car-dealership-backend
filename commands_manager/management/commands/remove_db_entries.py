from django.core.management.base import BaseCommand
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


class Command(BaseCommand):
    help = "Removing all database entries"

    def handle(self, *args, **kwargs):
        self._delete_all_objects(SupplierStockItem)
        self._delete_all_objects(DealerStockItem)
        self._delete_all_objects(SupplierDiscount)
        self._delete_all_objects(SupplierMarketingCampaign)
        self._delete_all_objects(DealerDiscount)
        self._delete_all_objects(DealerMarketingCampaign)
        self._delete_all_objects(CustomerOffer)
        self._delete_all_objects(CustomerDealsHistory)
        self._delete_all_objects(DealerDealsHistory)
        self._delete_all_objects(TotalDealerPurchase)
        self._delete_all_objects(TotalSupplierPurchase)
        self._delete_all_objects(Supplier)
        self._delete_all_objects(Dealer)
        self._delete_all_objects(Customer)
        self._delete_all_objects(Car)
        self._delete_all_objects(CarCharacteristic)
        self._delete_all_objects(UserProfile)

    def _delete_all_objects(self, model):
        model.objects.all().delete()
