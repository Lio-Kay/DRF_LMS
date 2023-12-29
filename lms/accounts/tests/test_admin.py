from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.admin import (UserAdmin, activate_user, deactivate_user,
                            set_default_avatar)
from accounts.models import CustomUser

User = get_user_model()


class AdminActionsTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(CustomUser, self.site)
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            avatar='/custom_avatar.png')

    def test_activate_user_action(self):
        self.user.is_active = False
        self.assertFalse(self.user.is_active)
        activate_user(self.user_admin, None, User.objects.all())
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_deactivate_user_action(self):
        self.assertTrue(self.user.is_active)
        deactivate_user(self.user_admin, None, User.objects.all())
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_set_default_avatar_action(self):
        self.assertNotEqual(
            self.user.avatar, '/path_to_default_avatar.jpg')
        set_default_avatar(self.user_admin, None, User.objects.all())
        self.user.refresh_from_db()
        self.assertEqual(
            self.user.avatar, '/path_to_default_avatar.jpg')
