from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from users.models import CustomUser
from .models import Habit

User = get_user_model()


class HabitAPITestCase(APITestCase):
    def setUp(self):
        # Создание пользователей для тестов
        self.client = APIClient()
        self.user = CustomUser.objects.create(user_id=1, password='testpassword')
        self.client.force_authenticate(user=self.user)

    def create_habit(self):
        # Вспомогательный метод для создания привычки
        url = '/habits/'
        data = {
            'place': 'петрова',
            'time': '2023-11-19T20:11:00',
            'action': 'гулять',
            'duration': '00:02:00',
            'frequency': '00:01:00'
        }
        response = self.client.post(url, data, format='json')
        return response

    def test_create_habit(self):
        # Тест создания привычки
        data = {'public': 'public', 'pleasantness': 'pleasant', 'duration': '00:02:00', 'frequency': '00:01:00'}
        response = self.create_habit(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().place, 'петрова')

    def test_update_habit(self):
        # Тест обновления привычки
        habit = Habit.objects.create(time='2023-11-19T20:11:00', public='public', pleasantness='pleasant',
                                     creator=self.user)
        data = {'pleasantness': 'unpleasant'}
        url = f'/habits/{habit.id}/'
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get().pleasantness, 'unpleasant')

    def test_delete_habit(self):
        # Тест удаления привычки
        habit = Habit.objects.create(time='2023-11-19T20:11:00', public='public', pleasantness='pleasant',
                                     creator=self.user)
        url = f'/habits/{habit.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_list_user_habits(self):
        # Тест получения списка привычек пользователя
        Habit.objects.create(time='2023-11-19T20:11:00', public='public', pleasantness='pleasant',
                             creator=self.user)
        Habit.objects.create(time='2023-11-19T20:11:00', public='public', pleasantness='pleasant',
                             creator=self.user)
        Habit.objects.create(time='2023-11-19T20:11:00', public='public', pleasantness='pleasant',
                             creator=self.user)
        Habit.objects.create(time='2023-11-19T20:11:00', public='public', pleasantness='pleasant',
                             creator=self.user)
        url = '/user/habits/'
        response = self.client.get(url)
        print(response.data['count'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
