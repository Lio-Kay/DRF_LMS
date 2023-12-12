from django.urls import path
from dj_rest_auth.views import (LoginView, LogoutView,
                                PasswordResetView, PasswordResetConfirmView, PasswordChangeView,
                                UserDetailsView)
from dj_rest_auth.registration.views import (RegisterView,
                                             VerifyEmailView, ResendEmailVerificationView)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

from accounts.apps import AccountsConfig


app_name = AccountsConfig.name

urlpatterns = [
    # Login and Logout URLs
    path('login/', LoginView.as_view(),
         name='login'),
    path('logout/', LogoutView.as_view(),
         name='logout'),
    # Password Reset URLs
    path('password/reset/', PasswordResetView.as_view(),
         name='password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # Registration URLs
    path('registration/', RegisterView.as_view(),
         name='register'),
    path('registration/verify-email/', VerifyEmailView.as_view(),
         name='verify_email'),
    path('registration/resend-email/', ResendEmailVerificationView.as_view(),
         name='resend_email'),
    # User URLs
    path('user/', UserDetailsView.as_view(),
         name='user_details'),
    path('user/password/', PasswordChangeView.as_view(),
         name='password_change'),
    # JWT
    path('token/obtain/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
]
