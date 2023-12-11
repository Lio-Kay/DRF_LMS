from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


NULLABLE = {'allow_null': True, 'allow_blank': True}


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    age = serializers.IntegerField(allow_null=True, required=False,
                                   min_value=12, max_value=120)
    gender_choices = [
        ('MALE', 'Мужчина'),
        ('FEMALE', 'Женщина'),
        ('OTHER', 'Предпочитаю не указывать'),
    ]
    gender = serializers.ChoiceField(**NULLABLE, required=False,
                                     choices=gender_choices, default='OTHER')
    phone = serializers.CharField(**NULLABLE, required=False)
    city = serializers.CharField(**NULLABLE, required=False,
                                 default='Не указан', max_length=100)
    avatar = serializers.ImageField(allow_null=True, required=False)

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
