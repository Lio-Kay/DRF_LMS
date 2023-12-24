from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    """Команда для создания суперпользователя"""
    help = ('Создает суперпользователя. Email: admin@admin.com, '
            'Phone: +1234567890, Password: admin')

    def handle(self, *args, **options):
        if User.objects.filter(email='admin@admin.com'):
            self.stderr.write(
                self.style.ERROR('Суперпользователь уже существует. '
                                 'Email: admin @ admin.com, '
                                 'Phone: +1234567890, Password: admin')
            )
            exit()

        user = User.objects.create_superuser(
            email='admin@admin.com',
            first_name='Admin',
            last_name='Admin',
            phone='+1234567890',
        )
        user.set_password('admin')
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f'Создали суперпользователя. Email: admin@admin.com, '
            'Phone: +1234567890, Password: admin')
        )
