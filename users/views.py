from rest_framework import generics
from .models import CustomUser
from .permissions import IsCurrentUser
from .serializers import UserSerializer, UserSerializerForOthers
from decouple import config
import telebot

bot = telebot.TeleBot(config('TELEBOT_API'))

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

#####################   Telegram    ###########################################


