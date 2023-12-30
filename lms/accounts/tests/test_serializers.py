from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

UserModel = get_user_model()


class CustomLoginSerializerTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='testuser@example.com',
            password='password123',
            phone='+12345678900',
            is_active=True,
        )
        self.email_address = EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            verified=True,)
        self.data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'phone': '+12345678900'
        }
        self.client = APIClient()

    def test_validate(self):
        # Успешный вход
        response = self.client.post(
            '/api/v1/dj-rest-auth/login/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        # Ошибка
        self.data['password'] = 'wrongpassword'
        response_invalid_credentials = self.client.post(
            '/api/v1/dj-rest-auth/login/', self.data, format='json')
        self.assertEqual(response_invalid_credentials.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertIn('Невозможно войти в систему с '
                      'указанными учётными данными.',
                      response_invalid_credentials.data['non_field_errors'])
