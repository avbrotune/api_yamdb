from rest_framework import permissions


class IsSuperOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == "admin"
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_staff
            or request.method in permissions.SAFE_METHODS
        )