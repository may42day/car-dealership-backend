from rest_framework import permissions
from common.permissions import IsProfileOwnerOrReadOnly

from users.models import UserProfile


class IsDealerOwner(permissions.BasePermission):
    """
    Object-level permission to only allow dealers to edit thier related objects.

    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        try:
            if request.user.dealer:
                dealer_id = view.kwargs.get("pk")
                return bool(
                    request.user.role == UserProfile.DEALER
                    and request.user.dealer.pk == int(dealer_id)
                )
        except UserProfile.dealer.RelatedObjectDoesNotExist:
            return False


class IsDealerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow customers to create or edit permissions.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.role == UserProfile.DEALER
        )


class IsDealerOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow dealers to create objects or edit only thier related objects.

    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role == UserProfile.DEALER

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.dealer.user_profile == request.user
