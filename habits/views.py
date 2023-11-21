from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Habit
from .pagination import HabitPagination
from .permissions import IsOwner, IsManager
from .serializers import HabitSerializer
from .services import create_periodic_task


class HabitViewSet(viewsets.ModelViewSet):
    """
    Представление для взаимодействия с привычками.

    Attributes:
    - `serializer_class`: Класс сериализатора для привычек.
    - `pagination_class`: Класс пагинации для списка привычек.
    - `queryset`: Набор данных для выборки публичных привычек.

    Methods:
    - `perform_create(serializer)`: Создание привычки и создание
    периодической задачи, если привычка неприятная.

    Permissions:
    - `get_permissions()`: Возвращает классы разрешений в
    зависимости от выполняемого действия.
    """
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    queryset = Habit.objects.filter(public='public')

    def perform_create(self, serializer):
        """
        Создание привычки и создание периодической задачи,
        если привычка неприятная.

        Parameters:
        - `serializer`: Сериализатор для привычки.
        """
        habit = serializer.save(creator=self.request.user)
        if habit.pleasantness == 'unpleasant':
            create_periodic_task(habit)

    def get_permissions(self):
        """
        Возвращает классы разрешений в зависимости от выполняемого действия.

        Returns:
        - `permissions`: Список классов разрешений.
        """
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwner | IsAdminUser | IsManager, ]
        elif self.action == 'delete' or self.action == 'create':
            permission_classes = [IsOwner, IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [IsOwner | IsAdminUser, IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class UsersHabitListAPIView(generics.ListAPIView):
    """
    Представление для получения списка привычек пользователя.

    Attributes:
    - `serializer_class`: Класс сериализатора для привычек.
    - `pagination_class`: Класс пагинации для списка привычек.
    - `permission_classes`: Классы разрешений, в данном случае,
    требуется аутентификация.

    Methods:
    - `get_queryset()`: Возвращает список привычек текущего пользователя.

    """
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает список привычек текущего пользователя.

        Returns:
        - `queryset`: Список привычек пользователя.
        """
        user = self.request.user
        return Habit.objects.filter(creator=user)
