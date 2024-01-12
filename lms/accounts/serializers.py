from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.conf import settings
from djoser.serializers import (UserSerializer, UserCreateMixin,
                                TokenCreateSerializer, UidAndTokenSerializer,
                                ActivationSerializer, PasswordSerializer,
                                PasswordRetypeSerializer,
                                CurrentPasswordSerializer, TokenSerializer)
from rest_framework import serializers
from rest_framework.settings import api_settings

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор пользователя

    Возвращает поля пользователя/пользователей
    email = models.EmailField()
    first_name = models.CharField()
    last_name = models.CharField()
    age = models.PositiveSmallIntegerField()
    gender = models.CharField()
    phone = PhoneNumberField()
    city = models.CharField()
    avatar = models.ImageField()

    #/users/ [name='customuser-list']
    #/users/<pk>/ [name='customuser-detail']
    #/users/me/ [name='customuser-me']
    """
    class Meta:
        model = User
        fields = ('pk', 'email', 'phone',
                  'first_name', 'last_name',
                  'age', 'gender', 'city', 'avatar',)
        read_only_fields = (settings.LOGIN_FIELD, 'phone',)


class CustomUserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    """
    Сериализатор регистрации нового пользователя

    Возвращает поля для заполнения:
    email = models.EmailField()
    first_name = models.CharField()
    last_name = models.CharField()
    age = models.PositiveSmallIntegerField()
    gender = models.CharField()
    phone = PhoneNumberField()
    city = models.CharField()
    avatar = models.ImageField()
    password = serializers.CharField()
    re_password = serializers.CharField()

    #/users/ [name='customuser-list']
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


class CustomTokenCreateSerializer(TokenCreateSerializer):
    """
    Сериализатор для получения DRF токена

    Возвращает поля для заполнения:
    password = serializers.CharField()
    email = models.EmailField()

    #token/login/ [name='login']
    """
    password = serializers.CharField(
        required=False, style={'input_type': 'password'}, label='Пароль')


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

    Возвращает поля для заполнения:
    uid = serializers.CharField()
    token = serializers.CharField()

    #/users/activation/ [name='customuser-activation']
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
    """
    re_new_password = serializers.CharField(
        style={'input_type': 'password'}, label='Повторите пароль')


class CustomCurrentPasswordSerializer(CurrentPasswordSerializer):
    """
    Сериализатор текущего пароля зарегистрированного пользователя
    """
    current_password = serializers.CharField(
        style={'input_type': 'password'}, label='Пароль')


class CustomTokenSerializer(TokenSerializer):
    """
    Сериализатор полученного DRF токена

    Возвращает поле с значением DRF токена
    auth_token = serializers.CharField()

    #token/login/ [name='login']
    """
    auth_token = serializers.CharField(
        source='key', label='Токен аутентификации')


class CustomSetPasswordRetypeSerializer(CustomCurrentPasswordSerializer,
                                        CustomPasswordRetypeSerializer):
    """
    Сериализатор изменения пароля зарегистрированного пользователя

    Возвращает поля для заполнения:
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()

    #users/set_password/  [name='customuser-set-password']
    """
    pass


class CustomPasswordResetConfirmRetypeSerializer(CustomUidAndTokenSerializer,
                                                 CustomPasswordRetypeSerializer):
    """
    Сериализатор сброса пароля зарегистрированного пользователя

    Возвращает поля для заполнения:
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()

    #users/reset_password_confirm/ [name='customuser-reset-password-confirm']
    """
    pass


class CustomUserDeleteSerializer(CustomCurrentPasswordSerializer):
    """
    Сериализатор удаления зарегистрированного пользователя

    Возвращает поля для заполнения:
    current_password = serializers.CharField()

    #users/me/ [name='customuser-me']
    """
    pass
