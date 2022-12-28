from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == User.RoleChoice.ADMIN)
                or request.user.is_superuser)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == User.RoleChoice.MODERATOR)
                or request.user.is_superuser)
