from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.apps import UsersConfig
from users.views import UserCreateListAPIView, UserRetrieveUpdateDestroyAPIView


app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
    path('', UserCreateListAPIView.as_view(),
         name='user_create-list'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(),
         name='user_retrieve-update-destroy'),
]
