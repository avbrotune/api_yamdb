from rest_framework import permissions


class IsSuperOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == request.user.ADMIN
            )
        )


class IsSuperOrIsAdminOrSafe(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == request.user.ADMIN
            )
            or request.method in permissions.SAFE_METHODS
        )


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user == obj.author
                or request.user.is_superuser
                or request.user.role == request.user.ADMIN
                or request.user.role == request.user.MODERATOR
            )
        )
