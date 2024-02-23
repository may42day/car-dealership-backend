from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import ConfirmationToken, UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.

    Allows conversion of UserProfile objects to/from JSON format.

    Parameters:
        - pk (int, read-only) - Primary Key for UserProfile model.
        - username (CharField, read-only) - user's username(login).
        - role (CharField, choices of USERS_ROLES, read-only) - user role (Customer/Dealer/Supplier).
        - first_name (CharField) - user's first name.
        - last_name (CharField) - user's last name.
        - email (EmailField, read-only) - user email address.
        - password (CharField) - user's password.
    """

    class Meta:
        model = UserProfile
        fields = [
            "pk",
            "username",
            "role",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        read_only_fields = ["pk"]
        write_only_fields = ["password"]


class UserProfileSerializer(UserRegisterSerializer):
    """
    Serializer for UserProfile model.
    Inherits from UserRegisterSerializer.

    Allows conversion of UserProfile objects to/from JSON format.

    Widen with parameters:
        - date_joined (DateTimeField, read-only) - represent date and time of user registration.
    """

    class Meta(UserRegisterSerializer.Meta):
        fields = UserRegisterSerializer.Meta.fields + [
            "date_joined",
        ]
        read_only_fields = UserRegisterSerializer.Meta.read_only_fields + [
            "role",
            "username",
        ]


class UserProfileOwnerSerializer(UserProfileSerializer):
    """
    Serializer for UserProfile model.
    Inherits from UserProfileSerializer.

    Allows conversion of UserProfile objects to/from JSON format.

    Widen with parameters:
        - is_staff (BooleanField, read-only) - indicates whether user have admin permissions.
        - is_active (BooleanField, read-only) - account status.
        - date_joined (DateTimeField, read-only) - represent date and time of user registration.
    """

    class Meta(UserRegisterSerializer.Meta):
        fields = UserRegisterSerializer.Meta.fields + [
            "is_staff",
            "is_active",
        ]
        read_only_fields = UserRegisterSerializer.Meta.read_only_fields + [
            "is_staff",
            "is_active",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for change user's password.

    Parameters:
        - old_password (CharField) - The user's current password.
        - new_password (CharField) - New password to set for user.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class TokenFromUrlSerializer(serializers.Serializer):
    """
    Serializer for getting token data from query parameters.

    Serializer is used to to extract and validate token and its type from query params in URL.

    Parameters:
        - token (CharField) - The user's current password.
        - token_type (CharField, choices) - Type of token (choices of TOKEN_TYPES in ConfirmationToken)

    Example of URL params:
        ?token=55ebb22f-3f93-45e4-8000-a1f71263431c&token_type=reg
    """

    token = serializers.CharField(required=True)
    token_type = serializers.CharField(required=True)


class EmailSerializer(serializers.Serializer):
    """
    Serializer for user's email.

    Serializer is used to validate email during password reset, login/email change.

    Parameters:
        - email (EmailField) - The user's email.

    """

    email = serializers.EmailField(required=True)


class PasswordResetSerializer(TokenFromUrlSerializer):
    """
    Serializer to reset user's password.
    Inherits from TokenFromUrlSerializer.

    Serializer is used after token validation to change user's password.

    Widen with parameters:
        - new_password (CharField) - New password to set for user.
    """

    new_password = serializers.CharField(required=True)


class EmailChangeSerializer(TokenFromUrlSerializer):
    """
    Serializer to change user's email.
    Inherits from TokenFromUrlSerializer.

    Serializer is used after token validation to change user's email.

    Widen with parameters:
        - new_email (CharField) - New email to set for user.
    """

    new_email = serializers.CharField(required=True)


class LoginChangeSerializer(TokenFromUrlSerializer):
    """
    Serializer to change user's login.
    Inherits from TokenFromUrlSerializer.

    Serializer is used after token validation to change user's login.

    Widen with parameters::
        - new_login (CharField) - New login to set for user.
    """

    new_username = serializers.CharField(required=True)
