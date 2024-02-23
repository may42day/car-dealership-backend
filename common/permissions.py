from rest_framework import permissions

from users.models import UserProfile


class IsCompanyOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow company-based users to edit thier related objects.
    Users with Dealer or Supplier role are related to company-based users.

    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.role in [UserProfile.DEALER, UserProfile.SUPPLIER])


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow company owners to edit thier related objects.
    Users with Dealer or Supplier role are related to companies owners.

    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile == request.user
