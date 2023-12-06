from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelCreateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            age=25,
            gender='MALE',
            phone='+1234567890',
            city='New York',
        )
        self.user.avatar.name = 'users/media/avatars/avatar.jpg'

    def tearDown(self):
        self.user.delete()

    def test_create_user(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.age, 25)
        self.assertEqual(self.user.gender, 'MALE')
        self.assertEqual(str(self.user.phone), '+1234567890')
        self.assertEqual(self.user.city, 'New York')
        self.assertEqual(self.user.avatar.name, 'users/media/avatars/avatar.jpg')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)


# TODO
# Make test passing
# class UserModelInvalidDataTestCase(TestCase):
#
#     def tearDown(self):
#         User.objects.all().delete()
#         try:
#             os.remove('users/avatars/avatar.txt')
#         except FileNotFoundError:
#             pass
#
#     def test_invalid_email(self):
#         with self.assertRaises(ValidationError):
#             User.objects.create_user(
#                 email='invalid_email',
#                 password='testpassword'
#             )
#
#     def test_age_validation(self):
#         with self.assertRaises(ValidationError):
#             User.objects.create_user(
#                 email='test@example.com',
#                 password='testpassword',
#                 age=10
#             )
#
#         with self.assertRaises(ValidationError):
#             User.objects.create_user(
#                 email='test@example.com',
#                 password='testpassword',
#                 age=130
#             )
#
#     def test_avatar_validation(self):
#         with self.assertRaises(ValidationError):
#             User.objects.create_user(
#                 email='test@example.com',
#                 password='testpassword',
#                 avatar=SimpleUploadedFile('avatar.txt', b'fake content')
#             )
