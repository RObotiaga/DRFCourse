from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Moderator').exists():
            return True

        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
