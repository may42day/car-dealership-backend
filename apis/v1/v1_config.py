from django.urls import path, include

urlpatterns = [
    path("cars/", include("cars.api.v1.urls")),
    path("customers/", include("customers.api.v1.urls")),
    path("dealers/", include("dealers.api.v1.urls")),
    path("marketing/", include("marketing.api.v1.urls")),
    path("orders/", include("orders.api.v1.urls")),
    path("suppliers/", include("suppliers.api.v1.urls")),
    path("users/", include("users.api.v1.urls")),
    path("stats/", include("stats.api.v1.urls")),
]
