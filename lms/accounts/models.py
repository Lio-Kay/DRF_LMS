from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    validate_image_file_extension)
from phonenumber_field.modelfields import PhoneNumberField

from accounts.apps import AccountsConfig


app_name = AccountsConfig.name

NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(BaseUserManager):
    """Кастомная модель для создания пользователя"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Введите email')
        if not password:
            raise ValueError('Введите пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Cуперпользователь должен иметь флаг is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Cуперпользователь должен иметь флаг is_superuser=True.')
        return self._create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    age = models.PositiveSmallIntegerField(**NULLABLE, verbose_name='Возраст',
                                           validators=[
                                               MinValueValidator(12),
                                               MaxValueValidator(120)
                                           ]
                                           )
    gender_choices = [
        ('MALE', 'Мужчина'),
        ('FEMALE', 'Женщина'),
        ('OTHER', 'Предпочитаю не указывать'),
    ]
    gender = models.CharField(**NULLABLE,
                              max_length=6,
                              choices=gender_choices,
                              default='OTHER',
                              verbose_name='Гендер')
    phone = PhoneNumberField(verbose_name='Телефон')
    city = models.CharField(**NULLABLE,
                            max_length=100,
                            verbose_name='Город')
    avatar = models.ImageField(**NULLABLE,
                               upload_to='users/media/avatars/',
                               verbose_name='Аватар',
                               validators=[
                                   validate_image_file_extension
                               ]
                               )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'first_name', 'last_name',

    def __str__(self):
        return f'{self.email, self.first_name, self.last_name}'

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'
        ordering = 'email',
