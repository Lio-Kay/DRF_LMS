from rest_framework import generics
from rest_framework.exceptions import NotFound

from payments.models import Payment
from payments.permissions import IsOwner
from payments.serializers import PaymentSerializer


class UserPaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Payment.objects.filter(user_id=user_id)


class UserPaymentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsOwner]

    def get_object(self):
        user_id = self.kwargs['user_id']
        payment_id = self.kwargs['payment_id']
        try:
            return Payment.objects.get(id=payment_id, user_id=user_id)
        except Payment.DoesNotExist:
            raise NotFound('Платеж не найден')
