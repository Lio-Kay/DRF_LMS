from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch

from accounts.views import VerifyEmailAPIView


UserModel = get_user_model()


class VerifyEmailAPIViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            email='testuser@example.com',
            password='password123'
        )
        self.key = 'test-key'

    @patch('requests.post')
    def test_verify_email_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = 'Email verification successful.'
        url = reverse('account_confirm_email', args=[self.key])
        request = self.factory.get(url)
        response = VerifyEmailAPIView.as_view()(request, self.key)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/v1/dj-rest-auth/user/')

    @patch('requests.post')
    def test_verify_email_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = 'Invalid email verification key.'
        url = reverse('account_confirm_email', args=[self.key])
        request = self.factory.get(url)
        response = VerifyEmailAPIView.as_view()(request, self.key)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/v1/dj-rest-auth/user/')
