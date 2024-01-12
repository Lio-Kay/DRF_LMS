from rest_framework import serializers

from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    paid_section = serializers.SerializerMethodField('get_paid_section')
    user = serializers.SerializerMethodField('get_user')

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
