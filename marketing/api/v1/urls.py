from rest_framework import routers
from django.urls import path, include

from marketing.api.v1 import views


router = routers.SimpleRouter()
router.register(
    r"dealers/campaigns",
    views.DealerMarketingCampaignAPIView,
    basename="dealers-marketing-campaign",
)
router.register(
    r"suppliers/campaigns",
    views.SuplierMarketingCampaignAPIView,
    basename="suppliers-marketing-campaign",
)
router.register(
    r"dealers/discounts", views.DealerDiscountsAPIView, basename="dealers-discounts"
)
router.register(
    r"suppliers/discounts",
    views.SuplierDiscountsAPIView,
    basename="suppliers-discounts",
)

urlpatterns = [
    path("", include(router.urls)),
]
