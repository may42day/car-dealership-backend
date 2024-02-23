from rest_framework import routers
from django.urls import path, include

from dealers.api.v1 import views


router = routers.SimpleRouter()
router.register(r"stock", views.DealerStockAPIView, basename="dealers-stock")
router.register(r"", views.DealerAPIView, basename="dealer")

urlpatterns = [
    path("<int:pk>/clients/deals", views.DealerClientsDealsAPIView.as_view()),
    path("<int:pk>/suppliers", views.DealerSuppliersListAPIView.as_view()),
    path("<int:pk>/suppliers/deals", views.DealerSuppliersDealsAPIView.as_view()),
    path("<int:pk>/discounts", views.DealerDiscountListAPIView.as_view()),
    path("<int:pk>/marketing-campaigns", views.DealerMarketingListAPIView.as_view()),
    path("", include(router.urls)),
]
