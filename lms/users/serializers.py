from rest_framework import serializers

from users.models import User


NULLABLE = {'allow_blank': True, 'allow_null': True, 'required': False}


class UserOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'email', 'password', 'first_name', 'last_name', 'age', 'gender', 'phone', 'city', 'avatar',
        extra_kwargs = {'password': {'write_only': True}}


class UserViewOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'first_name', 'city', 'avatar',
