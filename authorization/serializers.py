from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for JWT auth.
    Inherits from TokenObtainPairSerializer.

    Widen with two extra credentials for token:
    role : str
        represents user's role (Customer/Dealer/Supplier)
    is_staff : bool
        indicates whether user have admin permissions.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.role
        token["is_staff"] = user.is_staff
        return token
