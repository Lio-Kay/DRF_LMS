from django.urls import path, include

from accounts.apps import AccountsConfig

app_name = AccountsConfig.name

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
]
