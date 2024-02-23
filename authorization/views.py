from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import Token
import jwt

from authorization.serializers import CustomTokenObtainPairSerializer
from car_dealership.settings import SIMPLE_JWT


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    API view for JWT auth.
    Inherits from TokenObtainPairView.
    Uses custom serializer.

    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = CustomTokenObtainPairSerializer


class TokenDecodeView(APIView):
    """
    API view to decode auth token.

    Parse token from auth header and returns decoded data from token.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            decoded_data = jwt.decode(
                jwt=token,
                key=SIMPLE_JWT["SIGNING_KEY"],
                algorithms=[SIMPLE_JWT["ALGORITHM"]],
            )
            return Response(decoded_data, status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
