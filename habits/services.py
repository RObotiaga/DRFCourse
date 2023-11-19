from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone
from habits.models import Habit  # Замените "habits" на имя вашего приложения

def create_periodic_task(obj: Habit) -> None:
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=obj.frequency.total_seconds() // 60,
        period=IntervalSchedule.MINUTES,
    )

    current_time = timezone.now().time()
    if current_time < obj.time.time():
        start_time = datetime.combine(timezone.now().date(), obj.time.time())
    else:
        start_time = datetime.combine((timezone.now() + timedelta(days=1)).date(), obj.time.time())

    PeriodicTask.objects.create(
        interval=schedule,
        name=f"Habit_{obj.pk}",
        task='habits.tasks.enable_notifications',
        start_time=start_time,
        args=[obj.pk],
    )
