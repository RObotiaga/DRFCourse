from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Пользователь с правами Менеджера.

    Methods:
    - `has_permission(request, view)`:
    Проверяет, имеет ли пользователь права Менеджера.

    """
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Moderator').exists():
            return True

        return False


class IsOwner(BasePermission):
    """
    Владелец объекта.

    Methods:
    - `has_object_permission(request, view, obj)`:
    Проверяет, является ли пользователь владельцем объекта.

    """
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
