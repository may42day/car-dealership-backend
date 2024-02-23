from django.urls import path
from orders.api.v1 import views


urlpatterns = [
    path("customers/offers", views.CustomersOffersAPIView.as_view()),
    path("customers/offers/<int:pk>", views.CustomersOffersRetrieveAPIView.as_view()),
    path("customers/<int:pk>", views.CustomersDealsHistoryView.as_view()),
    path("customers", views.CustomersDealsHistoryView.as_view()),
    path("dealers/offers", views.DealersOffersAPIView.as_view()),
    path("dealers/offers/<int:pk>", views.DealersOffersRetrieveAPIView.as_view()),
    path(
        "dealers/<int:pk>/customers",
        views.DealersHistoryWithCustomersView.as_view(),
    ),
    path(
        "dealers/<int:pk>/customers/total",
        views.DealersTotalHistoryWithCustomersView.as_view(),
    ),
    path(
        "dealers/<int:pk>/suppliers",
        views.DealersHistoryWithSuppliersView.as_view(),
    ),
    path(
        "dealers/<int:pk>/suppliers/total",
        views.DealersTotalHistoryWithSuppliersView.as_view(),
    ),
    path(
        "suppliers/<int:pk>/dealers",
        views.SuppliersHistoryWithDealersView.as_view(),
    ),
    path(
        "suppliers/<int:pk>/total/dealers",
        views.SuppliersTotalPurchasesWithDealersView.as_view(),
    ),
]
