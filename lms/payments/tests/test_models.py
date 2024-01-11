from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from accounts.models import CustomUser
from education.models import Section
from payments.models import Payment


class PaymentModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            age=25,
            gender='MALE',
            phone='+1234567890',
            city='Test_City'
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

    def test_create_payment(self):
        payment_count = Payment.objects.count()
        self.assertEqual(payment_count, 1)
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.paid_section, self.section)
        self.assertEqual(self.payment.payment_type, 'SHARE_30D4P')
        self.assertEqual(self.payment.payment_method, 'STIPE')
        self.assertEqual(self.payment.payments_left, 3)
        self.assertAlmostEqual(self.payment.last_payment_date, timezone.now(),
                               delta=timedelta(seconds=1))

    def test_str_representation(self):
        # payments_left > 0
        expected_str = ('Пользователь: Test User testuser@example.com, '
                        'Курс: Test_Section, '
                        'Тип платежа: Долями. 30 дней. 4 платежа, '
                        'Осталось платежей: 3')
        self.assertEqual(str(self.payment), expected_str)
        # payments_left == 0
        self.payment.payments_left = 0
        expected_str = ('Пользователь: Test User testuser@example.com, '
                        'Курс: Test_Section, '
                        'Оплачен полностью')
        self.assertEqual(str(self.payment), expected_str)

    def test_clean_method(self):
        # Проверка отсутствия оставшихся платежей при полной оплате
        with self.assertRaises(ValidationError):
            payment = Payment.objects.create(
                user=self.user,
                paid_section=self.section,
                payment_type='FULL',
                payment_method='STIPE',
                payments_left=3,
            )
            payment.clean()
        payment = Payment.objects.create(
            user=self.user,
            paid_section=self.section,
            payment_type='FULL',
            payment_method='STIPE',
            payments_left=0,
        )
        payment.clean()
