from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class CustomUser(AbstractUser):
    """
    Модель пользователя.

    Attributes:
    - `user_id`: ИД пользователя в телеграм.
    """
    username = None
    user_id = models.BigIntegerField(verbose_name='ид пользователя',
                                     unique=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
