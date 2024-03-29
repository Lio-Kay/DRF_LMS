# Generated by Django 4.2.7 on 2024-01-21 09:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCardData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(validators=[django.core.validators.MinLengthValidator(16), django.core.validators.MaxLengthValidator(16)], verbose_name='Номер карты')),
                ('owner_name', models.CharField(max_length=100, verbose_name='Владелец')),
                ('expiration_month', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Месяц действия')),
                ('expiration_year', models.PositiveSmallIntegerField(verbose_name='Год действия')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'банковская карта',
                'verbose_name_plural': 'банковские карты',
                'db_table_comment': 'Модель банковской карты пользователя',
                'ordering': ('card_number',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('FULL', 'Полный'), ('SHARE_30D4P', 'Долями. 30 дней. 4 платежа')], max_length=11, verbose_name='Тип платежа')),
                ('payment_method', models.CharField(choices=[('STIPE', 'Ссылка STRIPE')], max_length=5, verbose_name='Способ платежа')),
                ('payments_left', models.PositiveSmallIntegerField(default=0, verbose_name='Кол-во оставшихся платежей')),
                ('last_payment_date', models.DateTimeField(auto_now=True, verbose_name='Дата последнего платежа')),
                ('paid_section', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments', to='education.section', verbose_name='Раздел')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
                'db_table_comment': 'Модель платежей за разделы',
                'order_with_respect_to': 'user',
            },
        ),
    ]
