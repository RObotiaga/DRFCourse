import telebot
from celery import shared_task
from decouple import config

from .models import Habit

bot = telebot.TeleBot(config('TELEBOT_API'))


@shared_task
def enable_notifications(pk: int) -> None:
    obj = Habit.objects.get(pk=pk)
    message = f'Пора выполнить привычку: {obj}\n' \
              f'Время на выполнение {obj.duration.total_seconds()} секунд'
    bot.send_message(obj.creator.user_id, message)
    print('message sent')
