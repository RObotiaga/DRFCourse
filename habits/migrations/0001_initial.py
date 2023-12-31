# Generated by Django 4.2.7 on 2023-11-19 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=30, verbose_name='место')),
                ('time', models.DateTimeField(verbose_name='время')),
                ('action', models.CharField(max_length=255, verbose_name='действие')),
                ('frequency', models.DurationField(default=datetime.timedelta(days=1), verbose_name='периодичность')),
                ('treasure', models.CharField(blank=True, max_length=255, null=True, verbose_name='вознаграждение')),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=60), verbose_name='длительность')),
                ('pleasantness', models.CharField(choices=[('pleasant', 'Приятная привычка'), ('unpleasant', 'Привычка')], default='unpleasant', verbose_name='приятность')),
                ('public', models.CharField(choices=[('public', 'Опубликовать'), ('not public', 'Не публиковать')], default='not public', verbose_name='публичность')),
            ],
            options={
                'verbose_name': 'привычка',
                'verbose_name_plural': 'привычки',
            },
        ),
    ]
