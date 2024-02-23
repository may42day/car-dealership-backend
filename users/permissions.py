from rest_framework import permissions


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow profile owners of profile to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.pk == request.user.pk
