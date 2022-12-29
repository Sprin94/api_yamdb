from rest_framework import permissions


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == User.RoleChoice.ADMIN
                or request.user.role == User.RoleChoice.MODERATOR)
