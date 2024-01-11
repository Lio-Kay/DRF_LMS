from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from education.models import Section
from payments.apps import PaymentsConfig

app_name = PaymentsConfig.name

NULLABLE = {'blank': True, 'null': True}

User = get_user_model()


class Payment(models.Model):
    """Модель платежей"""
    user = models.ForeignKey(
        to=User, on_delete=models.RESTRICT, verbose_name='Пользователь',
        related_name='payments')
    paid_section = models.ForeignKey(
        to=Section, on_delete=models.RESTRICT, verbose_name='Раздел',
        related_name='payments')

    payment_type_choices = [
        ('FULL', 'Полный'),
        ('SHARE_30D4P', 'Долями. 30 дней. 4 платежа'),
    ]
    payment_type = models.CharField(
        max_length=11, choices=payment_type_choices,
        verbose_name='Тип платежа')
    payment_method_choices = [
        ('STIPE', 'Ссылка STRIPE'),
    ]
    payment_method = models.CharField(
        max_length=5, choices=payment_method_choices,
        verbose_name='Способ платежа')
    payments_left = models.PositiveSmallIntegerField(
        default=0, verbose_name='Кол-во оставшихся платежей')
    last_payment_date = models.DateTimeField(
        auto_now=True, verbose_name='Дата последнего платежа')

    def __str__(self):
        if self.payments_left == 0:
            return (f'Пользователь: {self.user.first_name} '
                    f'{self.user.last_name} {self.user.email}, '
                    f'Курс: {self.paid_section}, '
                    f'Оплачен полностью')
        return (f'Пользователь: {self.user.first_name} '
                f'{self.user.last_name} {self.user.email}, '
                f'Курс: {self.paid_section}, '
                f'Тип платежа: {self.payment_type}, '
                f'Осталось платежей: {self.payments_left}')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        order_with_respect_to = 'user'
        db_table_comment = 'Модель платежей за разделы'

    def clean(self):
        # Проверка отсутствия оставшихся платежей при полной оплате
        if self.payment_type == 'FULL' and self.payments_left > 0:
            raise ValidationError('Полный платеж не может иметь '
                                  'оставшиеся платежи')
