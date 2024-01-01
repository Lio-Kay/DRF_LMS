from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """
    Команда для создания суперпользователя

    email=admin@admin.com,
    first_name=Admin,
    last_name=Admin,
    phone=+1234567890,
    password=admin
    """
    help = ('Создает суперпользователя.\n'
            'Email: admin@admin.com, Телефон: +12345678900, Пароль: admin')

    def handle(self, *args, **options):
        superuser = User.objects.get(email='admin@admin.com')
        correct_password = 'admin'
        if superuser:
            if check_password(correct_password, superuser.password):
                self.stderr.write(
                    self.style.ERROR('Суперпользователь уже существует')
                )
                exit()
            User.objects.get(email='admin@admin.com').delete()

        user = User.objects.create_superuser(
            email='admin@admin.com',
            first_name='Admin',
            last_name='Admin',
            phone='+12345678900',
        )
        user.set_password('admin')
        user.save()

        self.stdout.write(self.style.SUCCESS(
            'Создали суперпользователя.\n'
            'Email: admin@admin.com, Телефон: +12345678900, Пароль: admin')
        )
