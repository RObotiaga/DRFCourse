from rest_framework import generics
from .models import CustomUser
from .permissions import IsCurrentUser
from .serializers import UserSerializer, UserSerializerForOthers, UserRegisterSerializer
import logging

# ...

logger = logging.getLogger(__name__)

################################ API
class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if int(self.request.user.pk) == int(self.kwargs["pk"]):
            return UserSerializer
        else:
            return UserSerializerForOthers


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsCurrentUser]


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

#####################   Telegram    ###########################################
