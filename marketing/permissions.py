from rest_framework import permissions

from users.models import UserProfile


class IsMarketingDealerOwnerOrReadOnly(permissions.BasePermission):
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


class IsMarketingSupplierOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow suppliers to create objects or edit only thier related objects.

    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role == UserProfile.SUPPLIER

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.supplier.user_profile == request.user
