from rest_framework import routers
from django.urls import path, include

from suppliers.api.v1 import views


router = routers.SimpleRouter()
router.register(r"stock", views.SupplierStockAPIView, basename="suppliers-stock")
router.register(r"", views.SupplierAPIView, basename="supplier")

urlpatterns = [
    path("<int:pk>/clients", views.SuppliersClientsListAPIView.as_view()),
    path("<int:pk>/discounts", views.SupplierDiscountListAPIView.as_view()),
    path("<int:pk>/marketing-campaigns", views.SupplierMarketingListAPIView.as_view()),
    path("", include(router.urls)),
]
