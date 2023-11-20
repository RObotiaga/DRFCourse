from rest_framework import serializers
from .models import Habit
from .validators import max_duration, max_frequency


class HabitSerializer(serializers.ModelSerializer):
    read_only_fields = ('creator',)
    duration = serializers.DurationField(validators=[max_duration])
    frequency = serializers.DurationField(validators=[max_frequency])

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        treasure = data.get('treasure')
        pleasant_habit = data.get('pleasant_habit')
        pleasantness = data.get('pleasantness')
        related_habit = data.get('related_habit')

        if treasure and pleasant_habit:
            raise serializers.ValidationError(
                'Выберите либо Вознаграждение либо Полезную привычку,'
                ' не оба одновременно.')

        if (treasure or related_habit) and pleasantness:
            raise serializers.ValidationError(
                'У приятной привычки не может быть вознаграждения'
                ' или связанной привычки')

        if related_habit and related_habit.pleasantness != 'pleasant':
            raise serializers.ValidationError(
                'Связанная привычка должна быть приятной привычкой.')

        return data
