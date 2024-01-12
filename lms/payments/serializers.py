from rest_framework import serializers

from payments.models import Payment, UserCardData
from payments.validators import (ExpiryMonthValidator, ExpiryYearValidator,
                                 CVCValidator)


class PaymentSerializer(serializers.ModelSerializer):
    paid_section = serializers.SerializerMethodField(
        'get_paid_section', label='Оплаченный раздел')
    user = serializers.SerializerMethodField(
        'get_user', label='Пользователь')

    def get_paid_section(self, obj):
        return obj.paid_section.name

    def get_user(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name} {obj.user.email}'

    class Meta:
        model = Payment
        fields = ('pk', 'user', 'paid_section',
                  'payment_type', 'payment_method', 'payments_left',
                  'last_payment_date',)
        read_only_fields = ('payment_type', 'payment_method', 'payments_left',
                            'last_payment_date',)


class CardInfoSerializer(serializers.ModelSerializer):
    cvc = serializers.CharField(max_length=3, label='3-ый код')

    class Meta:
        model = UserCardData
        fields = ('pk', 'card_number', 'owner_name',
                  'expiration_month', 'expiration_year', 'cvc', 'user',)
        validators = [
            ExpiryMonthValidator(field='expiration_month'),
            ExpiryYearValidator(field='expiration_year'),
            CVCValidator(field='cvc'),
        ]
