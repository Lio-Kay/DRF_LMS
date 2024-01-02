from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.conf import settings
from djoser.serializers import (UserCreateMixin, UidAndTokenSerializer,
                                ActivationSerializer, PasswordSerializer,
                                PasswordRetypeSerializer)
from rest_framework import serializers
from rest_framework.settings import api_settings

User = get_user_model()


class CustomUserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    """
    Сериализатор регистрации нового пользователя
    #/users
    """
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, label='Пароль')
    re_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True,
        label='Повторите пароль')

    default_error_messages = {
        'cannot_create_user':
            settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR,
        'password_mismatch':
            settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR,
    }

    class Meta:
        model = User
        fields = ('email', 'password', 're_password', 'phone',
                  'first_name', 'last_name',
                  'age', 'gender', 'city', 'avatar',)

    def validate(self, attrs):
        self.fields.pop('re_password', None)
        re_password = attrs.pop('re_password')
        user = User(**attrs)
        password = attrs.get('password')

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {'password':
                     serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        if attrs['password'] == re_password:
            return attrs
        self.fail('password_mismatch')


class CustomUidAndTokenSerializer(UidAndTokenSerializer):
    """
    Сериализатор для ввода ID и токена верификации
    """
    uid = serializers.CharField(label='ID пользователя')
    token = serializers.CharField(label='Токен верификации')


class CustomActivationSerializer(CustomUidAndTokenSerializer,
                                 ActivationSerializer):
    """
    Сериализатор для активации нового пользователя данными из письма

    #/users/activation/
    """
    pass


class CustomPasswordSerializer(PasswordSerializer):
    """
    Сериализатор нового пароля активированного пользователя
    """
    new_password = serializers.CharField(
        style={'input_type': 'password'}, label='Новый пароль')


class CustomPasswordRetypeSerializer(CustomPasswordSerializer,
                                     PasswordRetypeSerializer):
    """
    Сериализатор добавления поля повторения пароля

    Расширяет сериализатор PasswordSerializer, добавляя проверку
    соответствия паролей
    """
    re_new_password = serializers.CharField(
        style={'input_type': 'password'}, label='Повторите пароль')


class CustomPasswordResetConfirmRetypeSerializer(CustomUidAndTokenSerializer,
                                                 CustomPasswordRetypeSerializer):
    """
    Сериализатор объединяющий ввод ID и токена верификации и пароля с проверкой

    #users/reset_password_confirm/
    """
    pass
