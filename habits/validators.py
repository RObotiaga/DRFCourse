from rest_framework import serializers


def max_duration(value):
    if value.total_seconds() > 120:
        raise serializers.ValidationError(
            'Длительность не должна превышать 120 секунд')


def max_frequency(value):
    if value.days > 7:
        raise serializers.ValidationError(
            'Нельзя выполнять привычку реже чем раз в 7 дней')
