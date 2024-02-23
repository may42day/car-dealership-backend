from django_filters import rest_framework as filters
import django_filters

from users.models import UserProfile


class UserFilter(filters.FilterSet):
    """
    A filter class for filtering UserProfile objects by different options.

    Filters
    -------
    - role: Filter users by their role (exact match, choices=UserProfile.USERS_ROLES).
    - date_joined__gt: Filter user profile with joined date is grater than specified value.
    - date_joined__lt: Filter user profile with joined date year is less than specified value.
    - is_active: Filter by active users (is_active is True).
    - is_staff: Filter by staff users (is_staff is True).
    """

    role = django_filters.ChoiceFilter(
        field_name="role",
        choices=UserProfile.USERS_ROLES,
    )
    date_joined__gt = django_filters.DateFilter(
        field_name="date_joined", lookup_expr="gt"
    )
    date_joined__lt = django_filters.DateFilter(
        field_name="date_joined", lookup_expr="lt"
    )

    class Meta:
        model = UserProfile
        fields = ["role", "is_active", "is_staff", "date_joined"]
