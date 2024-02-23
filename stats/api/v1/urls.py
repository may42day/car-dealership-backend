from django.urls import path, include
from stats.api.v1 import views

urlpatterns = [
    path(
        "customers/<int:pk>", views.CustomerStatsView.as_view(), name="customers-stats"
    ),
    path("dealers/<int:pk>", views.DealerStatsView.as_view(), name="dealers-stats"),
    path(
        "suppliers/<int:pk>", views.SupplierStatsView.as_view(), name="suppliers-stats"
    ),
]
