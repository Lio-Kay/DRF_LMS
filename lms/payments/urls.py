from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import UserPaymentListAPIView, UserPaymentDetailAPIView

app_name = PaymentsConfig.name

urlpatterns = [
    path('payments/<int:user_id>', UserPaymentListAPIView.as_view(),
         name='user_payments_list'),
    path('payments/<int:user_id>/<int:payment_id>/', UserPaymentDetailAPIView.as_view(),
         name='user_payment_detail'),
]
