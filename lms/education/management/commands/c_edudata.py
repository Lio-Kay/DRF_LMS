from django.core.management import BaseCommand
from django.utils.timezone import make_aware
from djmoney.money import Money
from faker import Faker


from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion, Test)


fake = Faker('ru_RU')


class Command(BaseCommand):
    """Команда для наполнения всех моделей приложения education"""
    help = 'Создает данные для приложения education'

    @staticmethod
    def get_creation_time():
        return make_aware(fake.past_datetime(
            start_date='-1y'))

    @staticmethod
    def get_update_time():
        return make_aware(fake.date_time_between(
            start_date='-6M', end_date='now'))

    def handle(self, *args, **options):

        Material.objects.all().delete()
        TestAnswer.objects.all().delete()
        TestQuestion.objects.all().delete()
        Test.objects.all().delete()

        # Media
        Media.objects.all().delete()
        media1 = Media.objects.create(
            name=fake.word(),
            creation_date=self.get_creation_time(),
            local_image=fake.file_name(extension='jpg'),
            external_image=fake.image_url(),
            )
        media2 = Media.objects.create(
            name=fake.word(),
            creation_date=self.get_creation_time(),
            local_video=fake.file_name(extension='mp4'),
            external_video=fake.url()
        )
        media3 = Media.objects.create(
            name=fake.word(),
            creation_date=self.get_creation_time(),
            local_audio=fake.file_name(extension='mp3'),
        )

        # Section
        Section.objects.all().delete()
        section1 = Section.objects.create(
            name=fake.word(),
            description=fake.paragraph(),
            status='ARCHIVED',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
            base_price=Money(fake.random_int(min=100, max=10000), 'RUB')
        )
        section1.media.add(media1)
        section2 = Section.objects.create(
            name=fake.word(),
            description=fake.paragraph(),
            status='CLOSED',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
            base_price=Money(fake.random_int(min=100, max=10000), 'RUB')
        )
        section2.media.add(media2)
        section3 = Section.objects.create(
            name=fake.word(),
            description=fake.paragraph(),
            status='CLOSED',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
            base_price=Money(fake.random_int(min=100, max=10000), 'RUB')
        )
        section3.media.add(media3)

        self.stdout.write(self.style.SUCCESS(
            f'Добавили данные для приложения education'))
