from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import (UserPaymentListAPIView, UserPaymentDetailAPIView,
                            UserPaySection)

app_name = PaymentsConfig.name

urlpatterns = [
    path('<int:user_pk>/', UserPaymentListAPIView.as_view(),
         name='user_payments_list'),
    path('<int:user_id>/<int:payment_pk>/', UserPaymentDetailAPIView.as_view(),
         name='user_payment_detail'),
    path('section_pay/<int:section_pk>/', UserPaySection.as_view(),
         name='user_pay')
]
