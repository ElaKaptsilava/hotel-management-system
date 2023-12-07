from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    """
    Custom permission to allow:
    1. Author of an object to edit it
    2. All users can get list an object's
    3. Authenticated user can create object.
    """

    def has_permission(self, request, view):
        if view.action == "list":
            return True
        elif view.action == "create":
            return request.user.is_authenticated
        elif view.action in ["retrieve", "update", "partial_update", "destroy"]:
            return request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action == ["update", "partial_update", "retrieve", "destroy"]:
            return obj == request.user
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin of an object to edit it.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
