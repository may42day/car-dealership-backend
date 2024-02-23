from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authorization.views import CustomTokenObtainPairView, TokenDecodeView

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/decode/", TokenDecodeView.as_view(), name="token_decode"),
]
