import requests
import telebot
from decouple import config
from .models import Habit
from celery import shared_task

bot = telebot.TeleBot(config('TELEBOT_API'))


@shared_task
def enable_notifications(pk: int, token=bot) -> None:
    obj = Habit.objects.get(pk=pk)
    message = f'Пора выполнить привычку: {obj}\nВремя на выполнение {obj.duration.total_seconds()} секунд'
    bot.send_message(obj.creator.user_id, message)
    print('message sent')
