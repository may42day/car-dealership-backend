from datetime import timedelta
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404

from car_dealership.settings import HOST_NAME, TOKEN_EXPIRATION_TIME_MINUTES
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, username, password, **extra_data):
        """
        Creates user with hashed password
        """
        if not username:
            raise ValueError("Username must be specified.")
        if not password:
            raise ValueError("Password must be specified.")

        user = self.model(username=username, **extra_data)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Creates superuser.
        """

        user = self.create_user(username=username, password=password, email=email)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user

    def block_user(self, user_id: int, new_status: bool = False):
        """
        Chanes user_profile is_active status and the same status for its related role profile.
        """
        user = get_object_or_404(UserProfile, pk=user_id)
        with transaction.atomic():
            user.is_active = new_status
            user.save()

            if user.role == UserProfile.CUSTOMER:
                user.customer_profile.is_active = new_status
                user.customer_profile.save()
            elif user.role == UserProfile.DEALER:
                user.dealer_profile.is_active = new_status
                user.dealer_profile.save()
            elif user.role == UserProfile.SUPPLIER:
                user.supplier_profile.is_active = new_status
                user.supplier_profile.save()


class UserProfile(AbstractUser):
    """
    A class to represent a user.
    Inherits from class AbstractUser.

    Attributes
    ----------
    role : CharField (choices from USERS_ROLES)
        user role
    is_active : BooleanField
        represent user's account status.
        Activates after email confirmation after registration.
    email : EmailField
        user's email address.

    Choices for 'role'
    ----------
    - Customer: Represents a customer.
    - Dealer:  Represents a dealer owner.
    - Supplier: Represents a supplier owner.
    """

    CUSTOMER = "customer"
    DEALER = "dealer"
    SUPPLIER = "supplier"

    USERS_ROLES = [
        (CUSTOMER, "Customer"),
        (DEALER, "Dealer"),
        (SUPPLIER, "Supplier"),
    ]

    role = models.CharField(max_length=8, choices=USERS_ROLES, default=CUSTOMER)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    objects = UserProfileManager()


class ConfirmationToken(models.Model):
    """
    A class to represent a token with its related data.

    Attributes
    ----------
    user : ForeignKey
        relation to UserProfile
    token : UUIDField
        unique token value.
    created_at : DateTimeField
        date and time when token was created.
    token_type : CharField
        type of token (choices from TOKEN_TYPES).

    Choices for 'token_type'
    ----------
    - reg: Represents a token for registration confirmation.
    - pas:  Represents a token for password reset.
    - log: Represents a token for login change.
    - em: Represents a token for email change.

    Methods
    ----------
    - is_valid. Checks whether the token is still valid.
    - create_link. Creates link based on the token type with token inside.
    """

    REG_CONFIRM = "reg"
    PASSW_RESET = "pas"
    LOGIN_CHANGE = "log"
    EMAIL_CHANGE = "em"

    TOKEN_TYPES = [
        (REG_CONFIRM, "Registration confirmation"),
        (PASSW_RESET, "Password reset"),
        (LOGIN_CHANGE, "Login change"),
        (EMAIL_CHANGE, "Email change"),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token_type = models.CharField(max_length=10, choices=TOKEN_TYPES)
    # ADD EMAIL UNIQUE

    def is_valid(self) -> bool:
        """
        Function to check whether the token is still valid.

        Returns:
            bool: True if token valid, False if not.
        """
        return timezone.now() - self.created_at < timedelta(
            minutes=TOKEN_EXPIRATION_TIME_MINUTES
        )

    def create_link(self):
        """
        Function to create link based on the token type with token inside.

        Returns:
            str: Generated link.
        """
        if self.token_type == self.REG_CONFIRM:
            base_link = reverse("reg-confirmation")
        else:
            base_link = reverse("check-token")

        params = f"?token={self.token}&token_type={self.token_type}"
        return f"{HOST_NAME}{base_link}{params}"
