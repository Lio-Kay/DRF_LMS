from rest_framework import serializers, exceptions
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import exceptions as url_exceptions


try:
    from allauth.account import app_settings as allauth_account_settings
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


NULLABLE = {'allow_null': True, 'allow_blank': True}

# Get the UserModel
UserModel = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(**NULLABLE,
                                   required=allauth_account_settings.EMAIL_REQUIRED,
                                   help_text='Электронная почта')
    phone = PhoneNumberField(**NULLABLE, required=False,
                             help_text='Номер телефона')
    password = serializers.CharField(style={'input_type': 'password'},
                                     help_text='Пароль')

    def _validate_phone(self, phone, password):
        if phone and password:
            user = self.authenticate(phone=phone, password=password)
        else:
            # TODO
            # Fix gettext_lazy
            msg = _('Must include "phone" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_allauth(self, username, email, password, phone):
        from allauth.account import app_settings as allauth_account_settings

        # Authentication through email OR PHONE
        if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.EMAIL:
            try:
                return self._validate_email(email, password)
            except exceptions.ValidationError:
                # Authentication through phone
                return self._validate_phone(phone, password)

        # Authentication through username
        if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.USERNAME:
            return self._validate_username(username, password)

        # Authentication through either username or email
        return self._validate_username_email(username, email, password)


    def get_auth_user_using_orm(self, username, email, password, phone):
        if email:
            try:
                username = UserModel.objects.get(email__iexact=email).get_username()
            except UserModel.DoesNotExist:
                pass

        if username:
            return self._validate_username_email(username, '', password)

        if phone:
            return self._validate_phone(phone, password)

        return None

    def get_auth_user(self, username, email, password, phone):
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.

        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if 'allauth' in settings.INSTALLED_APPS:

            # When `is_active` of a user is set to False, allauth tries to return template html
            # which does not exist. This is the solution for it. See issue #264.
            try:
                return self.get_auth_user_using_allauth(username, email, password, phone)
            except url_exceptions.NoReverseMatch:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        return self.get_auth_user_using_orm(username, email, password, phone)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        phone = attrs.get('phone')
        user = self.get_auth_user(username, email, password, phone)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)
        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user, email=email)

        attrs['user'] = user
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(
        required=allauth_account_settings.EMAIL_REQUIRED,
        help_text='Электронная почта')
    password1 = serializers.CharField(write_only=True, help_text='Пароль')
    password2 = serializers.CharField(write_only=True, help_text='Подтверждение пароля')
    first_name = serializers.CharField(max_length=50, help_text='Имя')
    last_name = serializers.CharField(max_length=50, help_text='Фамилия')
    age = serializers.IntegerField(allow_null=True, required=False,
                                   min_value=12, max_value=120,
                                   help_text='Возраст, от 12 до 120 лет')
    gender_choices = [
        ('MALE', 'Мужчина'),
        ('FEMALE', 'Женщина'),
        ('OTHER', 'Предпочитаю не указывать'),
    ]
    gender = serializers.ChoiceField(**NULLABLE, required=False,
                                     choices=gender_choices, initial='OTHER',
                                     help_text='Гендер')
    phone = PhoneNumberField(**NULLABLE, required=False,
                             help_text='Номер телефона')
    city = serializers.CharField(**NULLABLE, required=False,
                                 initial='Не указан', max_length=100,
                                 help_text='Город проживания')
    avatar = serializers.ImageField(allow_null=True, required=False,
                                    help_text='Фото профиля')

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'age': self.validated_data.get('age', ''),
            'gender': self.validated_data.get('gender', 'Предпочитаю не указывать'),
            'phone': self.validated_data.get('phone', ''),
            'city': self.validated_data.get('city', 'Не указан'),
            'avatar': self.validated_data.get('avatar', '/path_to_default_avatar.jpg'),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }
