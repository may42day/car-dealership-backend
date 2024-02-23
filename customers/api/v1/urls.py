from rest_framework import routers
from customers.api.v1 import views
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r"", views.CustomerAPIView, basename="customer")


urlpatterns = [
    path("<int:pk>/cars", views.CustomerCarsListAPIView.as_view()),
    path("<int:pk>/purchase-history", views.CustomerOrdersHistoryListAPIView.as_view()),
    path("", include(router.urls)),
]
