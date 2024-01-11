from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory

from accounts.models import CustomUser
from payments.admin import PaymentAdmin
from payments.models import Payment
from education.models import Section


class PaymentAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_site = AdminSite()
        self.payment_admin = PaymentAdmin(Payment, self.admin_site)
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            phone='+1234567890',
        )
        self.section = Section.objects.create(
            name='Test_Section',
            description='Test_Description',
            status='OPEN',
            creation_date='2023-01-01T00:00:00Z',
            last_update='2023-01-01T00:00:00Z',
            base_price=100,
        )
        self.payment = Payment.objects.create(
            user=self.user,
            paid_section=self.section,
            payment_type='SHARE_30D4P',
            payment_method='STIPE',
            payments_left=3,
        )

    def test_user_link(self):
        link = self.payment_admin.user_link(self.payment)
        expected_link = (f'<a href="/admin/accounts/customuser/'
                         f'{self.user.pk}/change/">'
                         f'Пользователь: Test User.</a>')
        self.assertEqual(link, expected_link)

    def test_empty_user_link(self):
        self.payment.user = None
        link = self.payment_admin.user_link(self.payment)
        expected_link = ''
        self.assertEqual(link, expected_link)
