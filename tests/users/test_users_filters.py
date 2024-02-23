from datetime import datetime
import pytest
import pytz
from ddf import G
from users.api.v1.serializers import UserProfileSerializer
from users.models import UserProfile


@pytest.fixture
@pytest.mark.django_db
def user_profile_data():
    """
    Fixture with user profile data to check filters.
    """
    date1 = datetime(2023, 1, 1, tzinfo=pytz.UTC)
    date2 = datetime(2023, 2, 2, tzinfo=pytz.UTC)
    date3 = datetime(2023, 11, 11, tzinfo=pytz.UTC)
    date4 = datetime(2023, 12, 12, tzinfo=pytz.UTC)
    user_profile1 = G(
        UserProfile,
        role=UserProfile.CUSTOMER,
        is_staff=True,
        is_active=True,
        date_joined=date1,
    )
    user_profile2 = G(
        UserProfile,
        role=UserProfile.CUSTOMER,
        is_staff=True,
        is_active=True,
        date_joined=date2,
    )
    user_profile3 = G(
        UserProfile,
        role=UserProfile.DEALER,
        is_staff=False,
        is_active=False,
        date_joined=date3,
    )
    user_profile4 = G(
        UserProfile,
        role=UserProfile.SUPPLIER,
        is_staff=False,
        is_active=False,
        date_joined=date4,
    )

    return {
        "user_profile1": user_profile1,
        "user_profile2": user_profile2,
        "user_profile3": user_profile3,
        "user_profile4": user_profile4,
    }


@pytest.mark.parametrize(
    "user_profile_keys, query_param, query_value",
    [
        (["user_profile1", "user_profile2"], "role", "customer"),
        (["user_profile3"], "role", "dealer"),
        (["user_profile4"], "role", "supplier"),
        (["user_profile1", "user_profile2"], "is_active", True),
        (["user_profile3", "user_profile4"], "is_active", False),
        (["user_profile1", "user_profile2"], "is_staff", True),
        (["user_profile3", "user_profile4"], "is_staff", False),
        (["user_profile1", "user_profile2"], "date_joined__lt", "2023-06-06"),
        (["user_profile3", "user_profile4"], "date_joined__gt", "2023-06-06"),
    ],
)
@pytest.mark.django_db
def test_user_profile_filters(
    api_client,
    user_profile_keys,
    query_param,
    query_value,
    user_profile_data,
):
    """
    Tests user profile filters.
    """
    data = {
        query_param: query_value,
    }
    response = api_client.get(
        f"/api/v1/users/",
        data=data,
        format="json",
    )

    serializer_data = UserProfileSerializer(
        [user_profile_data[key] for key in user_profile_keys],
        many=True,
    ).data

    assert response.data == serializer_data
