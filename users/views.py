import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .permissions import IsCurrentUser
from .serializers \
    import UserSerializer, UserSerializerForOthers, UserRegisterSerializer

logger = logging.getLogger(__name__)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
        Представление для получения информации о текущем пользователе.

        Parameters:
        - `queryset`: Набор данных для выборки пользователей.
        - `permission_classes`: Классы разрешений, в данном случае,
        требуется аутентификация.

        Methods:
        - `get_serializer_class()`: Возвращает класс сериализатора
        в зависимости от текущего пользователя.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsCurrentUser | IsAdminUser]

    def get_serializer_class(self):
        if self.request.user.pk == self.kwargs.get("pk"):
            return UserSerializer
        else:
            return UserSerializerForOthers


class UserUpdateAPIView(generics.UpdateAPIView):
    """
        Представление для обновления информации о текущем пользователе.

        Attributes:
        - `serializer_class`: Класс сериализатора для
        обновления данных о других пользователях.
        - `queryset`: Набор данных для выборки пользователей.
        - `permission_classes`: Классы разрешений, в данном случае,
        требуется, чтобы текущий пользователь был владельцем.

    """
    serializer_class = UserSerializerForOthers
    queryset = CustomUser.objects.all()
    permission_classes = [IsCurrentUser]


class UserCreateAPIView(generics.CreateAPIView):
    """
        Представление для создания нового пользователя.

        Attributes:
        - `queryset`: Набор данных для выборки пользователей.
        - `serializer_class`: Класс сериализатора для создания
        нового пользователя.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Представление для получения токенов доступа и обновления.

    Methods:
    - `post()`: Обработка POST-запроса для получения токенов.
    Добавляет дополнительное поле 'user_id' в данные запроса.

    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.
                Schema(type=openapi.TYPE_INTEGER,
                       description='ИД пользователя телеграм'),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['user_id', 'password'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запроса для получения токенов.

        Parameters:
        - `request`: Запрос с данными о пользователе и пароле.

        Returns:
        - `response`: Ответ с токенами доступа и обновления.
        """
        request.data['user_id'] = str(request.data.get('user_id', ''))
        response = super().post(request, *args, **kwargs)

        return response
