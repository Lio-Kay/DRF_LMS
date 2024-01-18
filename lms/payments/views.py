import icecream
import stripe
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from education.models import Section
from payments.models import Payment
from payments.permissions import IsOwner
from payments.serializers import PaymentSerializer, CardInfoSerializer


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


class UserPaySection(APIView):
    serializer_class = CardInfoSerializer
    stripe.api_key = settings.STRIPE_SECRET_API_KEY

    def post(self, request, section_pk):
        # Проверяем существование открытого раздела по pk
        try:
            section = Section.objects.get(pk=section_pk, status='OPEN')
        except ObjectDoesNotExist:
            return Response({
                'error': 'Открытий раздел с данным pk не найден',
                'requested_pk': section_pk,
                'available_pk': list(Section.objects.filter(status='OPEN').
                                     values_list('pk', flat=True))
            },
                status=status.HTTP_404_NOT_FOUND)
        # Получаем данные пользователя, отправившего запрос для сериализатора
        user_pk = request.user.pk
        request.data['user'] = request.user.pk
        # Проверяем, что раздел еще не оплачен
        user_payments = Payment.objects.get(
            user=user_pk, paid_section=section_pk)
        if user_payments.payments_left == 0:
            return Response({
                'error': 'Раздел уже оплачен',
                'requested_pk': section_pk,
            },
                status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data_dict = serializer.validated_data
            response = self.stripe_card_payment(
                data_dict=data_dict, section=section)
            icecream.ic(response)
        else:
            response = {
                'errors': serializer.errors,
                'status': status.HTTP_400_BAD_REQUEST,
            }
        return Response(response)

    def stripe_card_payment(self, data_dict, section):
        try:
            card_details = {
                'number': data_dict['card_number'],
                'exp_month': data_dict['expiration_month'],
                'exp_year': data_dict['expiration_year'],
                'cvc': data_dict['cvc'],
            }
            amount = int(section.base_price.amount * 100)
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='RUB',
                automatic_payment_methods={'enabled': True,
                                           'allow_redirects': 'never',},
            )
            try:
                payment_confirm = stripe.PaymentIntent.confirm(
                    payment_intent['id']
                )
                payment_intent_modified = stripe.PaymentIntent.retrieve(
                    payment_intent['id'])
            except Exception as e:
                payment_intent_modified = stripe.PaymentIntent.retrieve(
                    payment_intent['id'])
                # icecream.ic(payment_intent_modified)
                payment_confirm = {
                    'stripe_payment_error': 'Failed',
                    'code':
                        payment_intent_modified['last_payment_error']['code'],
                    'message':
                        payment_intent_modified['last_payment_error']
                        ['message'],
                    'status': 'Failed',
                }

            if (payment_intent_modified and payment_intent_modified['status']
                    == 'succeeded'):
                response = {
                    'message': 'Card Payment Success',
                    'status': status.HTTP_200_OK,
                    'card_details': card_details,
                    'payment_intent': payment_intent_modified,
                    'payment_confirm': payment_confirm,
                }
            else:
                response = {
                    'message': 'Card Payment Failed',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'card_details': card_details,
                    'payment_intent': payment_intent_modified,
                    'payment_confirm': payment_confirm,
                }
        except KeyError as e:
            response = {
                'error': 'Your card number is incorrect',
                'status': status.HTTP_400_BAD_REQUEST,
                'payment_intent': {'id': 'Null'},
                'payment_confirm': {'status': 'Failed'}
            }

        return response
