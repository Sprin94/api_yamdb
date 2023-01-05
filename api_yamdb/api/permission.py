from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == User.RoleChoice.ADMIN)
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS 
                or request.user.is_authenticated and request.user.role == 'admin'
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == User.RoleChoice.MODERATOR)
                or request.user.is_superuser)
