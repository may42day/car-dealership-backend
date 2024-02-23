from django.urls import path, include

urlpatterns = [
    path("v1/", include("apis.v1.v1_config")),
    path("auth/", include("authorization.urls")),
]
