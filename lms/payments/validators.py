from django.utils import timezone
from rest_framework import serializers


class CardNumberValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # Алгоритм Луна для номера карты на ошибки
        # https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%9B%D1%83%D0%BD%D0%B0
        data = dict(value).get(self.field, '')
        digits = [int(digit) for digit in data]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(
            odd_digits + [sum(divmod(digit * 2, 10)) for digit in even_digits])
        if not checksum:
            raise serializers.ValidationError(
                'Некорректный номер карты')


class ExpiryMonthValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data = dict(value).get(self.field, '')
        if not 1 <= int(data) <= 12:
            raise serializers.ValidationError('Карта просрочена')


class ExpiryYearValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data = dict(value).get(self.field, '')
        today = timezone.datetime.now()
        if not int(data) >= today.year:
            raise serializers.ValidationError('Карта просрочена')


class CVCValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data = dict(value).get(self.field, '')
        try:
            int(data)
        except ValueError:
            raise serializers.ValidationError(
                'CVC должен содержать только цифры')


class PaymentMethodValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        payment_method = value.lower()
        if payment_method not in ['card']:
            raise serializers.ValidationError('Неверный способ оплаты')
