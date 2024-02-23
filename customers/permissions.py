from rest_framework import permissions

from users.models import UserProfile


class IsCustomerOwner(permissions.BasePermission):
    """
    Object-level permission to only allow customers to edit only thier related objects.

    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.user.customer_profile:
            customer_id = view.kwargs.get("pk")
            return bool(
                request.user.role == UserProfile.CUSTOMER
                and request.user.customer_profile.pk == customer_id
            )


class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow customers to create or edit permissions.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.role == UserProfile.CUSTOMER
        )


class IsActiveUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow active customers to make offers.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or request.user.is_active is True
        )
