from django.urls import path, include
from rest_framework import routers

from cars.api.v1 import views

router = routers.SimpleRouter()
router.register(
    r"characteristics",
    views.CarCharacteristicAPIView,
    basename="characteristics",
)
router.register(
    r"",
    views.CarAPIView,
    basename="cars",
)

urlpatterns = [
    path("", include(router.urls)),
]
