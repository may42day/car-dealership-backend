from django.urls import path, include
from rest_framework import routers

from users.api.v1 import views

router = routers.SimpleRouter()
router.register(
    r"",
    views.UserAPIView,
    basename="users",
)


urlpatterns = [
    path("sign-up", views.UserRegistrationAPIView.as_view()),
    path(
        "sign-up/confirmation", views.ConfirmRegAPI.as_view(), name="reg-confirmation"
    ),
    path("reset-password", views.ResetPasswordAPI.as_view(), name="reset-password"),
    path(
        "reset-password/new",
        views.ProcessResetPasswordAPI.as_view(),
        name="process-password-reset",
    ),
    path("token/check", views.CheckTokenAPI.as_view(), name="check-token"),
    path("<int:pk>/block", views.UserBlockAPIView.as_view()),
    path("<int:pk>/change-email", views.ChangeEmailAPIView.as_view()),
    path("<int:pk>/change-email/new", views.ProcessChangeEmailAPIView.as_view()),
    path("<int:pk>/change-login", views.ChangeLoginAPIView.as_view()),
    path("<int:pk>/change-login/new", views.ProcessChangeLoginAPIView.as_view()),
    path("", include(router.urls)),
]
