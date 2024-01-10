# Generated by Django 4.2.7 on 2024-01-10 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('FULL', 'Полный'), ('SHARE_30D4P', 'Долями. 30 дней. 4 платежа')], max_length=11, verbose_name='Тип платежа'),
        ),
    ]
