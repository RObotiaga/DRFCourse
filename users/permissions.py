from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    """
    Текущий пользователь.

    Methods:
    - `has_permission(request, view)`:
    Проверяет, текущий ли пользователь сделал запрос.

    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj
