from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.urls import exceptions as url_exceptions
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, exceptions

try:
    from allauth.account import app_settings as allauth_account_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


NULLABLE = {'allow_null': True, 'allow_blank': True}

UserModel = get_user_model()


class CustomLoginSerializer(serializers.Serializer):
    """
    Кастомный LoginSerializer с поддержкой входа через email
    или номер телефона
    """
    email = serializers.EmailField(
        **NULLABLE, required=allauth_account_settings.EMAIL_REQUIRED,
        help_text='Электронная почта')
    phone = PhoneNumberField(
        **NULLABLE, required=False, help_text='Номер телефона')
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text='Пароль')

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email_phone(self, email, password, phone):
        if email and password:
            user = self.authenticate(email=email, password=password)
        elif phone and password:
            user = self.authenticate(phone=phone, password=password)
        else:
            raise exceptions.ValidationError(
                'Нужно указать пароль и почту или телефон')

        return user

    def get_auth_user_using_allauth(self, email, password, phone):
        from allauth.account import app_settings as allauth_account_settings

        if (allauth_account_settings.AUTHENTICATION_METHOD ==
                allauth_account_settings.AuthenticationMethod.EMAIL):
            # Аутентификация через почту или телефон
            return self._validate_email_phone(email, password, phone)
        raise ImportError('Allauth AuthenticationMethod не email')

    def get_auth_user(self, email, password, phone):
        if 'allauth' in settings.INSTALLED_APPS:
            try:
                return self.get_auth_user_using_allauth(email, password, phone)
            except url_exceptions.NoReverseMatch:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        raise ImportError('Allauth неправильно настроен или не установлен')

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_email_verification_status(user, email=None):
        from allauth.account import app_settings as allauth_account_settings
        if (
            allauth_account_settings.EMAIL_VERIFICATION == allauth_account_settings.EmailVerificationMethod.MANDATORY
            and not user.emailaddress_set.filter(email=user.email, verified=True).exists()
        ):
            raise serializers.ValidationError(_('E-mail is not verified.'))

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        phone = attrs.get('phone')
        user = self.get_auth_user(email, password, phone)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # Если пользователь активный
        self.validate_auth_user_status(user)

        # Если верификация почты обязательна, почта верифицирована?
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
        return {
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'age': self.validated_data.get('age', ''),
            'gender': self.validated_data.get('gender', ''),
            'phone': self.validated_data.get('phone', ''),
            'city': self.validated_data.get('city', ''),
            'avatar': self.validated_data.get('avatar', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }

    def custom_signup(self, request, user):
        # By default, django-allauth does not permit the preservation of custom fields
        user.age = self.cleaned_data.get('age')
        user.gender = self.cleaned_data.get('gender')
        user.phone = self.cleaned_data.get('phone')
        user.city = self.cleaned_data.get('city')
        user.avatar = self.cleaned_data.get('avatar')
        user.save()
        return user
