from unittest.mock import patch
import pytest

from django.db.models.signals import pre_save, post_save
from django_dynamic_fixture import G
from cars.models import Car

from customers.models import Customer
from dealers.models import Dealer, DealerStockItem
from marketing.models import (
    DealerDiscount,
    DealerMarketingCampaign,
    SupplierDiscount,
    SupplierMarketingCampaign,
)
from orders.models import TotalDealerPurchase, TotalSupplierPurchase
from suppliers.models import Supplier, SupplierStockItem
from users.models import UserProfile


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture(autouse=True)
def mute_signals(request):
    if "enable_signals" in request.keywords:
        return

    signals = [pre_save, post_save]
    restore = {}
    for signal in signals:
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals():
        for signal, receivers in restore.items():
            signal.receivers = receivers

    request.addfinalizer(restore_signals)


@pytest.fixture(autouse=True)
def disable_permissions(request, monkeypatch):
    """
    Patchs permissions to disable permissions for non-marked tests.
    To enable permissions test should be marked as '@pytest.mark.enable_permissions'.
    """

    def allow_all(*args, **kwargs) -> bool:
        return True

    if not "enable_permissions" in request.keywords:
        monkeypatch.setattr(
            "rest_framework.permissions.IsAuthenticated.has_permission", allow_all
        )
        monkeypatch.setattr(
            "rest_framework.permissions.IsAdminUser.has_permission", allow_all
        )
        monkeypatch.setattr(
            "rest_framework.permissions.IsAuthenticatedOrReadOnly.has_permission",
            allow_all,
        )
        monkeypatch.setattr(
            "users.permissions.IsProfileOwnerOrReadOnly.has_object_permission",
            allow_all,
        )
        monkeypatch.setattr(
            "common.permissions.IsProfileOwnerOrReadOnly.has_object_permission",
            allow_all,
        )
        monkeypatch.setattr(
            "customers.permissions.IsCustomerOwner.has_permission",
            allow_all,
        )
        monkeypatch.setattr(
            "dealers.permissions.IsDealerOwner.has_permission",
            allow_all,
        )
        monkeypatch.setattr(
            "suppliers.permissions.IsSupplierOwner.has_permission",
            allow_all,
        )

    yield


@pytest.fixture
@pytest.mark.django_db
def specific_customer():
    active_user = G(UserProfile, is_active=True)
    return G(Customer, user_profile=active_user, is_active=True)


@pytest.fixture
@pytest.mark.django_db
def other_customer():
    active_user = G(UserProfile, is_active=True)
    return G(Customer, user_profile=active_user)


@pytest.fixture
@pytest.mark.django_db
def admin_user():
    return G(UserProfile, is_staff=True, is_active=True)


@pytest.fixture
@pytest.mark.django_db
def other_user():
    return G(UserProfile, is_staff=False, is_active=True)


@pytest.fixture
@pytest.mark.django_db
def specific_user():
    user = G(UserProfile, role=UserProfile.CUSTOMER, is_staff=False, is_active=True)
    G(Customer, user_profile=user)
    return user


@pytest.fixture
@pytest.mark.django_db
def specific_dealer():
    user = G(UserProfile, is_active=True, role=UserProfile.DEALER)
    dealer = G(Dealer, user_profile=user)
    _discount = G(DealerDiscount, dealer=dealer)
    _marketing_campaign = G(DealerMarketingCampaign, dealer=dealer)
    return dealer


@pytest.fixture
@pytest.mark.django_db
def other_dealer():
    user = G(UserProfile, is_active=True, role=UserProfile.DEALER)
    dealer = G(Dealer, user_profile=user)
    _discount = G(DealerDiscount, dealer=dealer)
    _marketing_campaign = G(DealerMarketingCampaign, dealer=dealer)
    return dealer


@pytest.fixture
@pytest.mark.django_db
def specific_supplier():
    user = G(UserProfile, is_active=True, role=UserProfile.SUPPLIER)
    supplier = G(Supplier, user_profile=user)
    _discount = G(SupplierDiscount, supplier=supplier)
    _marketing_campaign = G(SupplierMarketingCampaign, supplier=supplier)
    return supplier


@pytest.fixture
@pytest.mark.django_db
def other_supplier():
    user = G(UserProfile, is_active=True, role=UserProfile.SUPPLIER)
    supplier = G(Supplier, user_profile=user)
    _discount = G(SupplierDiscount, supplier=supplier)
    _marketing_campaign = G(SupplierMarketingCampaign, supplier=supplier)
    return supplier


@pytest.fixture
def tr_data():
    """
    Fixture with with transaction data.
    """
    buyer_customer = G(Customer, balance=2000)
    buyer_dealer = G(Dealer, balance=20000)

    seller_dealer = G(Dealer, balance=14000)
    seller_supplier = G(Supplier, balance=80500)

    customer_total_purchases = G(
        TotalDealerPurchase, dealer=seller_dealer, customer=buyer_customer, amount=2
    )
    dealer_total_purchases = G(
        TotalSupplierPurchase, dealer=buyer_dealer, supplier=seller_supplier, amount=2
    )

    car = G(Car)

    stock_item_dealer = G(DealerStockItem, car=car, dealer=seller_dealer, amount=10)
    stock_item_supplier = G(
        SupplierStockItem, car=car, supplier=seller_supplier, amount=10
    )

    data = {
        "buyer_customer": buyer_customer,
        "buyer_dealer": buyer_dealer,
        "seller_dealer": seller_dealer,
        "seller_supplier": seller_supplier,
        "customer_total_purchases": customer_total_purchases,
        "dealer_total_purchases": dealer_total_purchases,
        "stock_item_dealer": stock_item_dealer,
        "stock_item_supplier": stock_item_supplier,
        "car": car,
        "price": 1000,
        "amount": 1,
    }
    return data


def parse_captured_queries_context(context) -> (int, int, int, int):
    """
    Function to pasrse queries into number for each SQL operation.
    """
    result = {
        "select": 0,
        "update": 0,
        "insert": 0,
    }

    for query in context.captured_queries:
        if query["sql"].startswith("INSERT INTO"):
            result["insert"] += 1

        elif query["sql"].startswith("UPDATE"):
            result["update"] += 1

        elif query["sql"].startswith("SELECT"):
            result["select"] += 1

    return (
        result["select"],
        result["update"],
        result["insert"],
        len(context.captured_queries),
    )
