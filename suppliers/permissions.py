from rest_framework import permissions

from users.models import UserProfile


class IsSupplierOwner(permissions.BasePermission):
    """
    Object-level permission to only allow suppliers to edit thier related objects.

    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        try:
            if request.user.supplier:
                supplier_id = view.kwargs.get("pk")
                return bool(
                    request.user.role == UserProfile.SUPPLIER
                    and request.user.supplier.pk == supplier_id
                )
        except UserProfile.supplier.RelatedObjectDoesNotExist:
            return False


class IsSupplierOwnerOrReadOnly(permissions.BasePermission):
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
