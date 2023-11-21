import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .permissions import IsCurrentUser
from .serializers \
    import UserSerializer, UserSerializerForOthers, UserRegisterSerializer

logger = logging.getLogger(__name__)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.pk == self.kwargs.get("pk"):
            return UserSerializer
        else:
            return UserSerializerForOthers


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializerForOthers
    queryset = CustomUser.objects.all()
    permission_classes = [IsCurrentUser]


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
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
        request.data['user_id'] = str(request.data.get('user_id', ''))
        response = super().post(request, *args, **kwargs)

        return response
