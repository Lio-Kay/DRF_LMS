from django.utils import timezone
from rest_framework import serializers


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
        today = timezone.datetime.now()
        if not int(value) >= today.year:
            raise serializers.ValidationError('Карта просрочена')


class CVCValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not 3 <= len(value) <= 4:
            raise serializers.ValidationError('Неверный трехзначный номер')


class PaymentMethodValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        payment_method = value.lower()
        if payment_method not in ['card']:
            raise serializers.ValidationError('Неверный способ оплаты')
