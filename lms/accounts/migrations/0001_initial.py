# Generated by Django 4.2.7 on 2024-01-21 09:56

import accounts.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(help_text='Не более 50 символов', max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Не более 50 символов', max_length=50, verbose_name='Фамилия')),
                ('age', models.PositiveSmallIntegerField(blank=True, help_text='Значение от 12 до 120', null=True, validators=[django.core.validators.MinValueValidator(12), django.core.validators.MaxValueValidator(120)], verbose_name='Возраст')),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'Мужчина'), ('FEMALE', 'Женщина'), ('OTHER', 'Предпочитаю не указывать')], default='OTHER', max_length=6, null=True, verbose_name='Гендер')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон')),
                ('city', models.CharField(blank=True, default='Не указан', help_text='Не более 100 символов', max_length=100, null=True, verbose_name='Город')),
                ('avatar', models.ImageField(blank=True, default='/path_to_default_avatar.jpg', null=True, upload_to='users/media/avatars/', validators=[django.core.validators.validate_image_file_extension], verbose_name='Аватар')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователя',
                'verbose_name_plural': 'пользователи',
                'db_table_comment': 'Кастомная и основная модель пользователя',
                'ordering': ('email',),
            },
            managers=[
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
    ]
