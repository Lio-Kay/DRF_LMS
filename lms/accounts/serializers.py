from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser import utils
from djoser.conf import settings
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

User = get_user_model()


class UserCreateMixin:
    """
    Миксин для UserCreateSerializer
    """
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=['is_active'])
        return user


class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    """
    Сериализатор регистрации нового пользователя
    #/users
    """
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, label='Пароль')
    re_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True,
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


class UidAndTokenSerializer(serializers.Serializer):
    """
    Сериализатор для ввода ID и токена верификации
    #/users/activation/
    """
    uid = serializers.CharField(label='ID пользователя')
    token = serializers.CharField(label='Токен верификации')

    default_error_messages = {
        'invalid_token': settings.CONSTANTS.messages.INVALID_TOKEN_ERROR,
        'invalid_uid': settings.CONSTANTS.messages.INVALID_UID_ERROR,
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        # uid validation have to be here, because validate_<field_name>
        # doesn't work with modelserializer
        try:
            uid = utils.decode_uid(self.initial_data.get('uid', ''))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = 'invalid_uid'
            raise ValidationError(
                {'uid': [self.error_messages[key_error]]},
                code=key_error
            )
        is_token_valid = self.context['view'].token_generator.check_token(
            self.user, self.initial_data.get('token', '')
        )
        if is_token_valid:
            return validated_data
        else:
            key_error = 'invalid_token'
            raise ValidationError(
                {'token': [self.error_messages[key_error]]},
                code=key_error
            )


class ActivationSerializer(UidAndTokenSerializer):
    """
    Сериализатор для активации нового пользователя данными из письма
    #/users/activation/
    """
    default_error_messages = {
        'stale_token': settings.CONSTANTS.messages.STALE_TOKEN_ERROR
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_active:
            return attrs
        raise exceptions.PermissionDenied(self.error_messages["stale_token"])
        raise exceptions.PermissionDenied(self.error_messages['stale_token'])
