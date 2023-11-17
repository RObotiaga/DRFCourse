from datetime import datetime, timedelta
from django.core.mail import send_mail
from celery import shared_task
# from .models import Subscription, Course
from users.models import CustomUser
from django.conf import settings


# @shared_task
# def send_notification(pk):
#     course = Course.objects.get(pk=pk)
#     subscription = Subscription.objects.filter(course=course)
#     users = [subscription.user.email for subscription in subscription]
#     print(users)
#     send_mail(
#         subject=f'Изменения в курсе "{course.name}"',
#         message=f'В курс "{course.name}" были внесены изменения',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=users,
#         fail_silently=False
#     )
#     print('all ok')
#

# def check_user_activity():
#     users = CustomUser.objects.filter(last_login__lt=datetime.now() - timedelta(days=30))
#     for user in users:
#         users.is_active = False
#         user.save()
#     users = CustomUser.objects.filter(last_login=None)
#     for user in users:
#         if user.date_joined < datetime.now() - timedelta(days=30):
#             users.is_active = False
#             user.save()
