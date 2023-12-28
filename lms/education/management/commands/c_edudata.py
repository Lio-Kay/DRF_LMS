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
        return make_aware(fake.date_time_between(
            start_date='-2y', end_date='-6M'))

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
            )
        media2 = Media.objects.create(
            name=fake.word(),
            creation_date=self.get_creation_time(),
            external_video=fake.url(),
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
            status='OPEN',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
            base_price=Money(fake.random_int(min=100, max=10000), 'RUB')
        )
        section3.media.add(media3)

        # Material
        Material.objects.all().delete()
        material1 = Material.objects.create(
            name=fake.word(),
            text=fake.paragraph(),
            status='ARCHIVED',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        material1.section = section1
        material1.save()
        material1.media.add(media1)
        material2 = Material.objects.create(
            name=fake.word(),
            text=fake.paragraph(),
            status='ARCHIVED',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        material2.section = section1
        material2.save()
        material2.media.add(media2)
        material3 = Material.objects.create(
            name=fake.word(),
            text=fake.paragraph(),
            status='CLOSED',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        material3.section = section2
        material3.save()
        material3.media.add(media3)
        material4 = Material.objects.create(
            name=fake.word(),
            text=fake.paragraph(),
            status='CLOSED',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        material4.section = section2
        material4.save()
        material4.media.add(media1)
        material5 = Material.objects.create(
            name=fake.word(),
            text=fake.paragraph(),
            status='OPEN',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        material5.section = section3
        material5.save()
        material5.media.add(media2)
        material6 = Material.objects.create(
            name=fake.word(),
            text=fake.paragraph(),
            status='OPEN',
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        material6.section = section3
        material6.save()
        material6.media.add(media3)

        # TestAnswer
        TestAnswer.objects.all().delete()
        testanswer1 = TestAnswer.objects.create(answer=fake.word())
        testanswer2 = TestAnswer.objects.create(answer=fake.word())
        testanswer3 = TestAnswer.objects.create(answer=fake.word())
        testanswer4 = TestAnswer.objects.create(answer=fake.word())
        testanswer5 = TestAnswer.objects.create(answer=fake.word())
        testanswer6 = TestAnswer.objects.create(answer=fake.word())

        # TestQuestion
        TestQuestion.objects.all().delete()
        testquestion1 = TestQuestion(
            question=fake.paragraph(),
            answer=testanswer1,
        )
        testquestion1.save()
        testquestion1.choices.add(testanswer1, testanswer2,
                                  testanswer3, testanswer4)
        testquestion1.media.add(media1)
        testquestion2 = TestQuestion(
            question=fake.paragraph(),
            answer=testanswer2,
        )
        testquestion2.save()
        testquestion2.choices.add(testanswer2, testanswer3,
                                  testanswer4, testanswer5)
        testquestion2.media.add(media2)
        testquestion3 = TestQuestion(
            question=fake.paragraph(),
            answer=testanswer3,
        )
        testquestion3.save()
        testquestion3.choices.add(testanswer3, testanswer4,
                                  testanswer5, testanswer6)
        testquestion3.media.add(media3)

        # Test
        Test.objects.all().delete()
        test1 = Test.objects.create(
            material=material1,
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        test1.question.add(testquestion1)
        test2 = Test.objects.create(
            material=material2,
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        test2.question.add(testquestion2)
        test3 = Test.objects.create(
            material=material3,
            creation_date=self.get_creation_time(),
            last_update=self.get_update_time(),
        )
        test3.question.add(testquestion3)

        self.stdout.write(self.style.SUCCESS(
            f'Добавили данные для приложения education'))
