from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import CustomUser


class UserAPITestCase(APITestCase):
    def setUp(self):
        # Создание пользователей для тестов
        self.client = APIClient()
        self.user1 = CustomUser.objects.create(user_id=1, password='testpassword')
        self.user2 = CustomUser.objects.create(user_id=2, password='testpassword')
        self.client.force_authenticate(user=self.user1)

    def test_retrieve_user_authenticated(self):
        # Тест получения информации о текущем пользователе (авторизованный)
        self.client.force_authenticate(user=self.user1)
        url = f'/{self.user1.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], self.user1.user_id)

    def test_update_user_authenticated(self):
        # Тест обновления информации о текущем пользователе (авторизованный)
        self.client.force_authenticate(user=self.user1)
        url = f'/edit/{self.user1.pk}/'
        data = {'password': '123'}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['password'], '123')

    def test_update_user_unauthorized(self):
        # Тест обновления информации о пользователе (неавторизованный)
        url = f'/edit/{self.user2.pk}/'
        data = {'some_field_to_update': 'new_value'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user(self):
        # Тест создания нового пользователя
        url = '/register/'
        print(url)
        data = {'user_id': 3, 'password': 'test_user'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_id'], 3)
