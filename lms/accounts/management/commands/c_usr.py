from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from faker import Faker

fake = Faker('ru_RU')
User = get_user_model()


class Command(BaseCommand):
    """Команда для удаления всех пользователей, кроме персонала и заполнения
    БД при помощи библиотеки Faker"""
    help = ('Удаляет всех пользователей, кроме персонала, и заполняет БД '
            'новыми пользователями')

    def handle(self, *args, **options):
        number_of_users = input('Какое кол-во пользователей добавить?\n')
        try:
            number_of_users = int(number_of_users)
        except ValueError:
            self.stderr.write(self.style.ERROR('Нечисловое значение'))
            exit()

        User.objects.filter(is_staff=False).delete()

        for user_num in range(number_of_users):
            user = User.objects.create(
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                age=fake.random_int(min=12, max=120),
                gender=fake.random_element(['MALE', 'FEMALE', 'OTHER']),
                phone=fake.phone_number(),
                city=fake.city(),
                avatar='/path_to_default_avatar.jpg',
            )
            user.set_password('1234')
            user.save()

        self.stdout.write(self.style.SUCCESS(
            f'Удалили всех пользователей, кроме персонала, и заполнили БД '
            f'{number_of_users} новыми пользователями')
        )
