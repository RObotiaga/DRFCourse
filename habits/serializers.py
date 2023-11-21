from rest_framework import serializers
from .models import Habit
from .validators import max_duration, max_frequency


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели привычек.

    Attributes:
    - `read_only_fields`: Поля, которые только для чтения .
    - `duration`: Поле для длительности привычки с валидатором `max_duration`.
    - `frequency`: Поле для частоты привычки с валидатором `max_frequency`.

    Methods:
    - `validate(data)`: Проверка дополнительных правил валидации
    данных перед сохранением.

    """
    read_only_fields = ('creator',)
    duration = serializers.DurationField(validators=[max_duration])
    frequency = serializers.DurationField(validators=[max_frequency])

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        """
        Проверка дополнительных правил валидации данных перед сохранением.

        Parameters:
        - `data`: Данные, полученные от клиента.

        Raises:
        - `ValidationError`: Исключение, если данные не проходят валидацию.

        Returns:
        - `data`: Валидные данные.

        """
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
