import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
import calendar

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
                    f'Курс: {self.paid_section.name}, '
                    f'Оплачен полностью')
        return (f'Пользователь: {self.user.first_name} '
                f'{self.user.last_name} {self.user.email}, '
                f'Курс: {self.paid_section.name}, '
                f'Тип платежа: {self.get_payment_type_display()}, '
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


class UserCardData(models.Model):
    """Модель банковской карты пользователя"""
    card_number = models.CharField(
        max_length=16, validators=[MinLengthValidator(16)],
        verbose_name='Номер карты')
    owner_name = models.CharField(max_length=100, verbose_name='Владелец')
    expiration_month = models.PositiveSmallIntegerField(
        max_length=12, validators=[MinLengthValidator(1)],
        verbose_name='Месяц действия')
    expiration_year = models.PositiveSmallIntegerField(
        verbose_name='Год действия')

    user = models.ForeignKey(to=User, on_delete=models.RESTRICT)

    def __str__(self):
        return (f'Номер карты: {self.card_number}, '
                f'Владелец: {self.owner_name}, '
                f'Срок действия: {self.expiration_month}/{self.expiration_year}')

    class Meta:
        verbose_name = 'банковская карта'
        verbose_name_plural = 'банковские карты'
        order = 'card_number'
        db_table_comment = 'Модель банковской карты пользователя'

    @staticmethod
    def validate_card_number(card_number):
        # Алгоритм Луна для проверки на ошибки
        digits = [int(digit) for digit in card_number]
        checksum = sum(digits[-1::-2] +
                       [sum(divmod(d * 2, 10)) for d in digits[-2::-2]])
        return checksum % 10 == 0

    def get_expiration_date(self):
        if self.expiration_month and self.expiration_year:
            last_day_of_month = calendar.monthrange(
                self.expiration_year, self.expiration_month)[1]
            return timezone.datetime.date(
                self.expiration_year, self.expiration_month, last_day_of_month)

    @staticmethod
    def validate_latin_characters(text):
        return bool(re.match('^[a-zA-Z\s]+$', text))

    def clean(self):
        # Валидация номера карты по алгоритму Луна
        if not self.validate_card_number(self.card_number):
            raise ValidationError(
                {'card_number': 'Ошибка в номере карты'})
        # Валидация срока действия
        expiration_date = self.get_expiration_date()
        if expiration_date and expiration_date < timezone.now().date():
            raise ValidationError(
                {'expiration_month': 'Срок действия карты истек'})
        # Валидация латинских символов в имени владельца
        if not self.validate_latin_characters(self.owner_name):
            raise ValidationError(
                {'owner_name': 'Имя владельца должно быть на латинице'})
