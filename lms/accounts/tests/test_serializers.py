from django.test import TestCase
from rest_framework.exceptions import ValidationError

from accounts.serializers import CustomUserCreateSerializer


class CustomUserCreateSerializerTest(TestCase):

    def setUp(self):
        self.data = {
            'email': 'testuser@example.com',
            'password': 'good_password',
            're_password': 'bad_password',
            'first_name': 'Test',
            'last_name': 'User',
            'age': 25,
            'gender': 'MALE',
            'phone': '+1234567890',
            'city': 'Test_City',
        }
        self.serializer = CustomUserCreateSerializer(data=self.data)

    def test_validate_method(self):
        with self.assertRaises(ValidationError):
            self.serializer.validate(self.data)
