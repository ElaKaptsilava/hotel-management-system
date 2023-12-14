from rest_framework import permissions


class PermissionHandler(permissions.BasePermission):
    """
    Handles permission checks for API views.

    - `has_permission`: Determines if a user has permission for a specific view action.
    - `has_object_permission`: Determines if a user has permission for a specific object.

    Usage:
    - Use `has_permission` to validate permissions based on view actions (e.g., list, create).
    - Use `has_object_permission` to validate permissions for specific objects (e.g., update, retrieve).

    Note:
    - Assumes that `request.user` represents the current user.
    - Returns `True` if permission is granted, otherwise `False`.
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
        if request.user.is_staff:
            return True
        if view.action == ["update", "partial_update", "retrieve", "destroy"]:
            return obj == request.user
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission class to control access based on user authentication and staff status.

    Allows read-only access (GET, HEAD, OPTIONS) for all users, but only allows modification
    (POST, PUT, PATCH, DELETE) if the user is authenticated, has staff privileges, and is not anonymous.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_staff
            and request.user.is_authenticated
        )
