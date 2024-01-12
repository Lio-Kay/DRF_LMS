from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from education.models import Section
from payments.models import Payment

User = get_user_model()


class Command(BaseCommand):
    """Команда для удаления всех данных из payments и
     наполнения всех моделей"""
    help = 'Удаляет все данные из payments, и заполняет БД новыми данными'

    def handle(self, *args, **options):

        Payment.objects.all().delete()
        Payment.objects.create(
            user=User.objects.filter(is_staff=False).order_by('?').first(),
            paid_section=Section.objects.order_by('?').first(),
            payment_type='FULL',
            payment_method='STIPE',
            payments_left=0,
        )
        Payment.objects.create(
            user=User.objects.filter(is_staff=False).order_by('?').first(),
            paid_section=Section.objects.order_by('?').first(),
            payment_type='FULL',
            payment_method='STIPE',
            payments_left=0,
        )
        Payment.objects.create(
            user=User.objects.filter(is_staff=False).order_by('?').first(),
            paid_section=Section.objects.order_by('?').first(),
            payment_type='SHARE_30D4P',
            payment_method='STIPE',
            payments_left=4,
        )
        Payment.objects.create(
            user=User.objects.filter(is_staff=False).order_by('?').first(),
            paid_section=Section.objects.order_by('?').first(),
            payment_type='SHARE_30D4P',
            payment_method='STIPE',
            payments_left=1,
        )

        self.stdout.write(self.style.SUCCESS(
            'Добавили данные для приложения payments'))
