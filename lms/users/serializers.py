from rest_framework import serializers

from users.models import CustomUser


NULLABLE = {'allow_blank': True, 'allow_null': True, 'required': False}


class UserOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = 'email', 'password', 'first_name', 'last_name', 'age', 'gender', 'phone', 'city', 'avatar',


class UserViewOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = 'first_name', 'city', 'avatar',
