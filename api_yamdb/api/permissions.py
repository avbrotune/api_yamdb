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


class TitlePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return True
        elif view.action == ['create', 'partial_update', 'destroy']:
            return request.user or request.user.is_admin
