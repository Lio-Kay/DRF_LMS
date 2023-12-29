from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import CustomUser

UserModel = get_user_model()


class CustomUserManagerTest(TestCase):
    def setUp(self):
        self.manager = UserModel.objects

    def test_create_user(self):
        user = self.manager.create_user('testuser@example.com', 'password123')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            self.manager.create_user(None, 'password123')

    def test_create_user_no_password(self):
        with self.assertRaises(ValueError):
            self.manager.create_user('testuser@example.com', None)

    def test_create_superuser(self):
        user = self.manager.create_superuser('admin@example.com',
                                             'password123')
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_no_staff(self):
        with self.assertRaises(ValueError):
            self.manager.create_superuser('admin@example.com',
                                          'password123', is_staff=False)

    def test_create_superuser_no_superuser(self):
        with self.assertRaises(ValueError):
            self.manager.create_superuser('admin@example.com',
                                          'password123', is_superuser=False)


class CustomUserTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            age=25,
            gender='MALE',
            phone='+1234567890',
            city='Test City'
        )

    def tearDown(self):
        self.user.delete()

    def test_create_user(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.age, 25)
        self.assertEqual(self.user.gender, 'MALE')
        self.assertEqual(self.user.phone, '+1234567890')
        self.assertEqual(self.user.city, 'Test City')
        self.assertTrue(self.user.check_password('password123'))

    def test_str_representation(self):
        self.assertEqual(str(self.user),
                         "('testuser@example.com', 'Test', 'User')")

    def test_age_validation(self):
        with self.assertRaises(ValidationError):
            self.user.age = 10
            self.user.full_clean()

        with self.assertRaises(ValidationError):
            self.user.age = 121
            self.user.full_clean()

    def test_avatar_validation(self):
        with self.assertRaises(ValidationError):
            self.user.avatar = 'invalid_image.txt'
            self.user.full_clean()
