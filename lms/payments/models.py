from django.contrib.auth import get_user_model
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
    last_payment_date = models.DateTimeField(
        auto_now=True, verbose_name='Дата последней оплаты')
    paid_section = models.ForeignKey(
        **NULLABLE, to=Section, on_delete=models.SET_NULL,
        related_name='payments')
    payment_type_choices = [
        ('FULL', 'Полная'),
        ('SHARE_30D4P', 'Долями. 30 дней. 4 оплаты'),
    ]
    payment_type = models.CharField(
        max_length=11, choices=payment_type_choices,
        verbose_name='Тип оплаты')
    payment_method_choices = [
        ('STIPE', 'Ссылка STRIPE'),
    ]
    payment_method = models.CharField(
        max_length=5, choices=payment_method_choices,
        verbose_name='Способ оплаты')
    payments_left = models.PositiveSmallIntegerField(
        default=0, verbose_name='Кол-во оставшихся оплат')

    def __str__(self):
        if self.payments_left == 0:
            return (f'Пользователь: {self.user.first_name} '
                    f'{self.user.last_name}, '
                    f'Курс: {self.paid_section}, '
                    f'Оплачен полностью')
        return (f'Пользователь: {self.user.first_name} '
                f'{self.user.last_name}, '
                f'Курс: {self.paid_section}, '
                f'Тип оплаты: {self.payment_type} '
                f'Осталось оплат: {self.payments_left}')

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
        ordering = 'paid_section',
