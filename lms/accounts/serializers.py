from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField

try:
    from allauth.account import app_settings as allauth_account_settings
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


NULLABLE = {'allow_null': True, 'allow_blank': True}


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
