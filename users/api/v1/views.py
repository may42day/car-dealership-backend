from rest_framework import mixins, viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from users.api.v1.serializers import (
    ChangePasswordSerializer,
    EmailChangeSerializer,
    EmailSerializer,
    LoginChangeSerializer,
    PasswordResetSerializer,
    TokenFromUrlSerializer,
    UserProfileOwnerSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
)
from users.filters import UserFilter
from users.models import ConfirmationToken, UserProfile
from users.tasks import email_change_email, email_change_login, email_reset_password
from users.permissions import IsProfileOwnerOrReadOnly


class BaseTokenMixin:
    """
    Mixin to get ConfirmationToken object or raise 404 error.
    """

    def get_object(self, token, token_type):
        return get_object_or_404(ConfirmationToken, token=token, token_type=token_type)


class BaseEmailMixin:
    """
    Mixin to get UserProfile object or raise 404 error.
    """

    def get_object(self, email):
        return get_object_or_404(UserProfile, email=email)


class UserAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    User endpoint.

    This endpoint provides CRUD operations for users.

    Includes filtering and ordering UserProfile objects.

    HTTP methods:
    - GET
    - POST
    - PUT
    - PATCH

    Request parameters:
    - id (path parameter, optional)

    Actions:
    -GET : Retrieve a list of all users.
    -GET : Retrieve a user's detail.
    -PUT/PATCH : Update users's data by ID.
    -POST [<pk:int>/change-password]: Change password.
    """

    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["date_joined"]
    filterset_class = UserFilter

    def get_serializer_class(self):
        """
        Function to get serializer class based on request user.
        """
        if self.request.user.is_staff:
            return UserProfileOwnerSerializer
        elif "pk" in self.kwargs and self.request.user.pk == int(self.kwargs.get("pk")):
            return UserProfileOwnerSerializer
        return UserProfileSerializer

    @action(methods=["post"], detail=True, url_path="change-password")
    def change_password(self, request, pk=None):
        """
        Change password for UserProfile.

        Function to change user password if old is correct.

        HTTP methods:
            - POST

        Request parameters:
            - id (path parameter) - user's id for whom password changes

        Request(JSON):
        {
            "password_old": "current_password",
            "password_new": "new_password"
        }

        Returns:
            - 200 OK: Password has been changed.
            - 400 Bad request: There are errors during password change.

        """
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_pass = serializer.validated_data["old_password"]
            new_pass = serializer.validated_data["new_password"]

            if user.check_password(old_pass):
                user.set_password(new_pass)
                user.save()
                return Response(
                    {"message": "Password has been changed"}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBlockAPIView(APIView):
    """
    API to block or unblock user.

    HTTP methods:
    - PUT: block the user.
    - DELETE: unblock the user.

    Request parameters:
    - pk (path parameter): user's id.

    Returns:
    - 200 OK: user has been successfully blocked or unblocked.
    - 404 Not Found: User doesn't exists.
    """

    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        """
        Api to block a user.

        Blocks a user account by setting its 'is_active' attribute to False.

        Request parameters:
            pk (int): user's id.

        Returns:
        - 200 OK: user has been successfully blocked.
        - 404 Not Found: User doesn't exists.
        """

        UserProfile.objects.block_user(pk)
        return Response({"message": "User blocked"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Api to unblock a user.

        Unblocks a user account by setting its 'is_active' attribute to True.

        Request parameters:
            pk (int): user's id.

        Returns:
        - 200 OK: user has been successfully unblocked.
        - 404 Not Found: User doesn't exists.
        """

        UserProfile.objects.block_user(pk, new_status=True)
        return Response({"message": "User unblocked"}, status=status.HTTP_200_OK)


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    API for users registration.

    HTTP methods:
    - POST: Create a new user profile.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Creates UserProfile with hashed password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserProfile.objects.create_user(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConfirmRegAPI(BaseTokenMixin, APIView):
    """
    API for confirm account registration.

    Checks token in get params and activates account.

    HTTP methods:
    - Get: Confirm account registration.

    Request parameters:
    - token (query parameter): The confirmation token.
    - token_type (query parameter): The type of the confirmation token.

    Returns:
    - 200 OK: If the user registration account confirmed.
    - 400 Bad request: If token is invalid.
    - 403 Forbidden: If the token is expired.
    - 404 Not Found: If token object does not exist.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Confirm user registration.

        Checks token in get params and activates account.
        """
        serializer = TokenFromUrlSerializer(data=request.GET)

        if serializer.is_valid():
            token = self.get_object(
                serializer.validated_data["token"],
                serializer.validated_data["token_type"],
            )

            if token.is_valid():
                token.user.is_active = True
                token.user.save()
                return Response(
                    {"message": "Registration confirmed"}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Token expired"}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckTokenAPI(BaseTokenMixin, APIView):
    """
    API to check whether token is valid.

    Checks token in get params.

    HTTP methods:
    - Get: Check whether token is valid.

    Request parameters:
    - token (query parameter): The confirmation token.
    - token_type (query parameter): The type of the confirmation token.

    Returns:
    - 200 OK: If token is still valid and not expired.
    - 400 Bad request: If token is invalid.
    - 403 Forbidden: If the token is expired.
    - 404 Not Found: If token object does not exist.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Validates and checks token.
        """
        serializer = TokenFromUrlSerializer(data=request.GET)

        if serializer.is_valid():
            token = self.get_object(
                serializer.validated_data["token"],
                serializer.validated_data["token_type"],
            )

            if token.is_valid():
                return Response(
                    {"message": "Token is valid", "token_type": token.token_type},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Token expired", "token_type": token.token_type},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# APIs for password reset
class ResetPasswordAPI(BaseEmailMixin, APIView):
    """
    API to send email with instructions to reset user's password.

    Checks email and create task with sending email with instructions to reset password.

    HTTP methods:
    - POST: Create task with instructions.

    Request parameters:
    - email (EmailField) - The user's email.

    Returns:
    - 200 OK: If email has been sent.
    - 400 Bad request: If the email is invalid.
    - 404 Not Found: If user object with current email does not exist.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Create task with sending email with instructions to reset password.
        """
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            user = self.get_object(serializer.validated_data["email"])

            email_reset_password.delay(user.pk)
            return Response(
                {"message": "Instructions has been sent to email"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcessResetPasswordAPI(APIView, BaseTokenMixin):
    """
    API to handle password reset after token validation.

    Checks token and then changes user's password

    HTTP methods:
    - POST: Reset user's password.

    Request parameters:
    - new_password (CharField) - New password to set for user.
    - token (CharField) - Token to reset password.
    - token_type (CharField, choices) - Type of token (choices of TOKEN_TYPES in ConfirmationToken)

    Returns:
    - 200 OK: If password has been changed.
    - 400 Bad request: If token is invalid.
    - 403 Forbidden: If the token is expired.
    - 404 Not Found: If token object does not exist.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Validates token and then changes user password.
        """
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            token = self.get_object(
                serializer.validated_data["token"],
                serializer.validated_data["token_type"],
            )

            if token.is_valid() and token.token_type == token.PASSW_RESET:
                user = token.user
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response(
                    {"message": "Password has been changed"}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Token expired"}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# APIs for email change
class ChangeEmailAPIView(BaseEmailMixin, APIView):
    """
    API to send email with instructions to change user's email.

    Checks email and create task with sending email with instructions to change email.

    HTTP methods:
    - POST: Create task with instructions.

    Request parameters:
    - email (EmailField) - The user's email.

    Returns:
    - 200 OK: If email has been sent.
    - 400 Bad request: If the email is invalid.
    - 404 Not Found: If user object with current email does not exist.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        """
        Validates email and then create task with sending email.
        """
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            user = self.get_object(serializer.validated_data["email"])

            email_change_email.delay(user.pk)
            return Response(
                {"message": "Instructions has been sent to email"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcessChangeEmailAPIView(BaseTokenMixin, APIView):
    """
    API to handle email change after token validation.

    Checks token and then changes user's email

    HTTP methods:
    - POST: Change user's email.

    Request parameters:
    - new_email (CharField) - New email to set for user.
    - token (CharField) - Token to change email.
    - token_type (CharField, choices) - Type of token (choices of TOKEN_TYPES in ConfirmationToken)

    Returns:
    - 200 OK: If email has been changed.
    - 400 Bad request: If token is invalid.
    - 403 Forbidden: If the token is expired.
    - 404 Not Found: If token object does not exist.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        """
        Validates token and then changes user email.
        """
        serializer = EmailChangeSerializer(data=request.data)

        if serializer.is_valid():
            token = self.get_object(
                serializer.validated_data["token"],
                serializer.validated_data["token_type"],
            )

            if token.is_valid() and token.token_type == token.EMAIL_CHANGE:
                user = token.user
                user.email = serializer.validated_data["new_email"]
                user.save()
                return Response(
                    {"message": "Email has been changed"}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Token expired"}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# APIs for login change
class ChangeLoginAPIView(BaseEmailMixin, APIView):
    """
    API to send email with instructions to change user's login.

    Checks email and create task with sending email with instructions to change login.

    HTTP methods:
    - POST: Create task with instructions.

    Request parameters:
    - email (EmailField) - The user's email.

    Returns:
    - 200 OK: If email has been sent.
    - 400 Bad request: If the email is invalid.
    - 404 Not Found: If user object with current email does not exist.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        """
        Validates email and then create task with sending email.
        """
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            user = self.get_object(serializer.validated_data["email"])

            email_change_login.delay(user.pk)
            return Response(
                {"message": "Instructions has been sent to email"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProcessChangeLoginAPIView(BaseTokenMixin, APIView):
    """
    API to handle login change after token validation.

    Checks token and then changes user's login

    HTTP methods:
    - POST: Change user's login.

    Request parameters:
    - new_login (CharField) - New login to set for user.
    - token (CharField) - Token to change login.
    - token_type (CharField, choices) - Type of token (choices of TOKEN_TYPES in ConfirmationToken)

    Returns:
    - 200 OK: If login has been changed.
    - 400 Bad request: If token is invalid.
    - 403 Forbidden: If the token is expired.
    - 404 Not Found: If token object does not exist.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        """
        Validates token and then changes user login.
        """
        serializer = LoginChangeSerializer(data=request.data)

        if serializer.is_valid():
            token = self.get_object(
                serializer.validated_data["token"],
                serializer.validated_data["token_type"],
            )

            if token.is_valid() and token.token_type == token.LOGIN_CHANGE:
                user = token.user
                user.username = serializer.validated_data["new_username"]
                user.save()
                return Response(
                    {"message": "Username has been changed"}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Token expired"}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
