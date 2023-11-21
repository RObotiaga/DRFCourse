from datetime import timedelta

from django.db import models
from users.models import CustomUser
from dateutil.parser import parse
NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Habit(models.Model):
    """
    Модель для представления привычек.

    Attributes:
    - `creator`: Пользователь, создавший привычку.
    - `place`: Место, где осуществляется привычка.
    - `time`: Время выполнения привычки.
    - `action`: Описание действия, связанного с привычкой.
    - `pleasant_habit`: Связанная полезная привычка (может быть null).
    - `related_habit`: Связанная привычка (может быть null).
    - `frequency`: Периодичность выполнения привычки.
    - `treasure`: Вознаграждение за выполнение привычки (может быть null).
    - `duration`: Длительность выполнения привычки (по умолчанию, 1 минута).
    - `pleasantness`: Уровень приятности привычки.
    - `public`: Статус публичности привычки ('public' или 'not public').
    """
    creator = models.ForeignKey(CustomUser, verbose_name='создатель',
                                on_delete=models.CASCADE, blank=True)
    place = models.CharField(max_length=30, verbose_name='место')
    time = models.DateTimeField(verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие')
    pleasant_habit = models.ForeignKey('self',
                                       verbose_name='полезная привычка',
                                       on_delete=models.DO_NOTHING,
                                       related_name='pleasant_habits',
                                       **NULLABLE)
    related_habit = models.ForeignKey('self',
                                      verbose_name='связанная привычка',
                                      on_delete=models.DO_NOTHING,
                                      related_name='related_habits',
                                      **NULLABLE)
    frequency = models.DurationField(verbose_name='периодичность',
                                     default=timedelta(hours=24))
    treasure = models.CharField(max_length=255,
                                verbose_name='вознаграждение', **NULLABLE)
    duration = models.DurationField(verbose_name='длительность',
                                    default=timedelta(minutes=1))
    pleasantness = models.CharField(choices=[('pleasant', 'Приятная привычка'),
                                             ('unpleasant', 'Привычка')],
                                    default='unpleasant',
                                    verbose_name='приятность')
    public = models.CharField(choices=[('public', 'Опубликовать'),
                                       ('not public', 'Не публиковать')],
                              default='not public',
                              verbose_name='публичность')

    def __str__(self):
        return f'{self.action} в ' \
               f'{parse(str(self.time)).strftime("%Y-%m-%d %H:%M")}' \
               f' в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
