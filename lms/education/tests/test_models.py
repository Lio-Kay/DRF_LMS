from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion, Test)


class MediaModelTests(TestCase):
    maxDiff = None

    def setUp(self):
        self.media = Media.objects.create(
            name='Test_Media',
            creation_date='2023-01-01T00:00:00Z',
            external_image='https://example.com/image.jpg',
        )

    def tearDown(self):
        self.media.delete()

    def test_create_media(self):
        media_count = Media.objects.count()
        self.assertEqual(media_count, 1)
        self.assertEqual(self.media.name, 'Test_Media')
        self.assertEqual(
            self.media.external_image,
            'https://example.com/image.jpg')

    def test_str_representation(self):
        expected_str = ('Название: Test_Media, '
                        'Дата создания: 2023-01-01T00:00:00Z, '
                        'Медиа: https://example.com/image.jpg')
        self.assertEqual(str(self.media), expected_str)

    def test_clean_method(self):
        # Проверка на обязательный выбор только одного медиа файла
        media = Media(name='Test_Media')
        with self.assertRaises(ValidationError):
            media.clean()
        media = Media(
            name='Test_Media',
            local_image='path/to/image.jpg',
            external_image='https://example.com/image.jpg',
        )
        with self.assertRaises(ValidationError):
            media.clean()
        media = Media(
            name='Test_Media',
            local_image='path/to/image.jpg',
            local_video='path/to/video.mp4',
        )
        with self.assertRaises(ValidationError):
            media.clean()
        media = Media(
            name='Test_Media',
            local_image='path/to/image.jpg',
            external_audio='https://example.com/audio.mp3',
        )
        with self.assertRaises(ValidationError):
            media.clean()
        # Выполнение метода без ошибок
        media = Media(
            name='Test_Media',
            local_audio='path/to/audio.mp3',
        )
        media.clean()

    def test_save_method(self):
        # Автозапись даты создания
        media = Media.objects.create(name='Test_Media')
        self.assertEqual(media.creation_date.date(), timezone.now().date())


class SectionModelTests(TestCase):
    def setUp(self):
        self.media = Media.objects.create(name='Test_Media')
        self.section = Section.objects.create(
            name='Test_Section',
            description='Test_Description',
            status='OPEN',
            creation_date='2023-01-01T00:00:00Z',
            last_update='2023-01-01T00:00:00Z',
            base_price=100,
        )
        self.section.media.add(self.media)

    def tearDown(self):
        self.section.delete()
        self.media.delete()

    def test_create_section(self):
        section_count = Section.objects.count()
        self.assertEqual(section_count, 1)
        self.assertEqual(self.section.name, 'Test_Section')
        self.assertEqual(self.section.description, 'Test_Description')
        self.assertEqual(self.section.status, 'OPEN')
        self.assertEqual(self.section.creation_date,
                         '2023-01-01T00:00:00Z')
        self.assertEqual(self.section.last_update,
                         '2023-01-01T00:00:00Z')
        self.assertEqual(self.section.base_price.amount, 100)
        self.assertIn(self.media, self.section.media.all())

    def test_str_representation(self):
        expected_str = ('Название: Test_Section, Статус: Открытый, '
                        'Дата создания: 2023-01-01T00:00:00Z, '
                        'Базовая цена: 100,00\xa0₽')
        self.assertEqual(str(self.section), expected_str)

    def test_status_choices_auto_set(self):
        section = Section.objects.create(name='Test_Section')
        self.assertEqual(section.status, 'CLOSED')

    def test_constraint(self):
        # Проверка даты обновления позже или с одинаковой с датой создания
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Section.objects.create(
                    name='Test_Section',
                    creation_date=timezone.now(),
                    last_update=timezone.now() - timedelta(days=1),
                )

    def test_clean_method(self):
        # Проверка даты обновления позже или с одинаковой с датой создания
        with self.assertRaises(IntegrityError):
            with self.assertRaises(ValidationError):
                with transaction.atomic():
                    Section.objects.create(
                        name='Test_Section',
                        creation_date=timezone.now(),
                        last_update=timezone.now() - timedelta(days=1),
                    )
        section = Section.objects.create(
            name='Test_Section',
            status='ARCHIVED',
            creation_date=timezone.now(),
            last_update=timezone.now(),
        )
        section.clean()
        section = Section.objects.create(
            name='Test_Section',
            status='ARCHIVED',
            creation_date=timezone.now() - timedelta(days=1),
            last_update=timezone.now(),
        )
        section.clean()

    def test_save_method(self):
        # Автозапись даты создания
        section = Section.objects.create(name='Test_Section')
        self.assertEqual(section.creation_date.date(), timezone.now().date())
        # Автозапись даты обновления
        self.assertEqual(section.last_update.date(), timezone.now().date())


class MaterialModelTests(TestCase):
    def setUp(self):
        self.section = Section.objects.create(name='Test_Section')
        self.media = Media.objects.create(name='Test_Media')
        self.material = Material.objects.create(
            name='Test_Material',
            text='Test_Text',
            status='CLOSED',
            creation_date='2023-01-01T00:00:00Z',
            last_update='2023-01-01T00:00:00Z',
            section=self.section
        )
        self.material.media.add(self.media)

    def tearDown(self):
        self.material.delete()
        self.section.delete()
        self.media.delete()

    def test_create_material(self):
        material_count = Material.objects.count()
        self.assertEqual(material_count, 1)
        self.assertEqual(self.material.name, 'Test_Material')
        self.assertEqual(self.material.text, 'Test_Text')
        self.assertEqual(self.material.status, 'CLOSED')
        self.assertEqual(self.material.creation_date,
                         '2023-01-01T00:00:00Z')
        self.assertEqual(self.material.last_update,
                         '2023-01-01T00:00:00Z')
        self.assertEqual(self.material.section, self.section)
        self.assertIn(self.media, self.material.media.all())

    def test_str_representation(self):
        expected_str = ('Название: Test_Material, '
                        'Статус: Закрытый, '
                        'Дата создания: 2023-01-01T00:00:00Z')
        self.assertEqual(str(self.material), expected_str)

    def test_status_choices_auto_set(self):
        material = Section.objects.create(name='Test_Material')
        self.assertEqual(material.status, 'CLOSED')

    def test_constraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Material.objects.create(
                    name='Test_Material',
                    creation_date=timezone.now(),
                    last_update=timezone.now() - timedelta(days=1)
                )

    def test_clean_method(self):
        section = Section.objects.create(
            name='Test_Section',
            status='ARCHIVED')

        # Проверка даты обновления позже или с одинаковой с датой создания
        with self.assertRaises(IntegrityError):
            with self.assertRaises(ValidationError):
                with transaction.atomic():
                    material = Material.objects.create(
                        name='Test_Material',
                        status='ARCHIVED',
                        creation_date=timezone.now(),
                        last_update=timezone.now() - timedelta(days=1),
                        section=section,
                    )
                    material.clean()
        material = Material.objects.create(
            name='Test_Material',
            status='ARCHIVED',
            creation_date=timezone.now(),
            last_update=timezone.now(),
            section=section,
        )
        material.clean()
        material = Material.objects.create(
            name='Test_Material',
            status='ARCHIVED',
            creation_date=timezone.now() - timedelta(days=1),
            last_update=timezone.now(),
            section=section,
        )
        material.clean()

        # Проверка на соответствие статуса материала статусу раздела
        material = Material(
            name='Test_Material',
            status='OPEN',
            creation_date=timezone.now() - timedelta(days=1),
            last_update=timezone.now(),
            section=section,
        )
        with self.assertRaises(ValidationError):
            material.clean()
        section.status = 'CLOSED'
        with self.assertRaises(ValidationError):
            material.clean()

    def test_save_method(self):
        material = Material.objects.create(name='Test_Material')
        self.assertEqual(material.creation_date.date(), timezone.now().date())
        self.assertEqual(material.last_update.date(), timezone.now().date())


class TestAnswerModelTests(TestCase):
    def setUp(self):
        self.answer = TestAnswer.objects.create(answer='Test_Answer')

    def tearDown(self):
        self.answer.delete()

    def test_create_answer(self):
        answer_count = TestAnswer.objects.count()
        self.assertEqual(answer_count, 1)
        self.assertEqual(self.answer.answer, 'Test_Answer')

    def test_str_representation(self):
        expected_str = 'Ответ: Test_Answer'
        self.assertEqual(str(self.answer), expected_str)


class TestQuestionModelTests(TestCase):
    def setUp(self):
        self.answer1 = TestAnswer.objects.create(answer='Test_Answer1')
        self.answer2 = TestAnswer.objects.create(answer='Test_Answer2')
        self.media = Media.objects.create(name='Test_Media')
        self.testquestion = TestQuestion.objects.create(
            question='Test_Question',
            answer=self.answer1)
        self.testquestion.choices.add(self.answer1)
        self.testquestion.choices.add(self.answer2)
        self.testquestion.media.add(self.media)

    def tearDown(self):
        self.answer1.delete()
        self.answer2.delete()
        self.media.delete()
        self.testquestion.delete()

    def test_question_creation(self):
        question_count = TestQuestion.objects.count()
        self.assertEqual(question_count, 1)
        self.assertEqual(self.testquestion.question, 'Test_Question')
        self.assertEqual(self.testquestion.answer, self.answer1)
        self.assertIn(self.media, self.testquestion.media.all())

    def test_str_representation(self):
        expected_str = 'Вопрос: Test_Question, Ответ: Test_Answer1'
        self.assertEqual(str(self.testquestion), expected_str)


class TestModelTests(TestCase):
    def setUp(self):
        self.material = Material.objects.create(name='Test_Material')
        self.test_answer1 = TestAnswer.objects.create(answer='Answer1')
        self.test_answer2 = TestAnswer.objects.create(answer='Answer2')
        self.test_question = TestQuestion.objects.create(
            question='Question',
            answer=self.test_answer1)
        self.test_question.choices.add(self.test_answer1, self.test_answer2)
        self.test = Test.objects.create(
            material=self.material,
            creation_date='2023-01-01T00:00:00Z',
            last_update='2023-01-01T00:00:00Z',
        )
        self.test.question.add(self.test_question)

    def tearDown(self):
        self.material.delete()
        self.test_answer1.delete()
        self.test_answer2.delete()
        self.test_question.delete()
        self.test.delete()

    def test_create_test(self):
        tests_count = Test.objects.count()
        self.assertEqual(tests_count, 1)
        self.assertEqual(self.test.material, self.material)
        self.assertEqual(self.test.creation_date,
                         '2023-01-01T00:00:00Z')
        self.assertEqual(self.test.last_update,
                         '2023-01-01T00:00:00Z')
        self.assertEqual(self.test.question.count(), 1)
        self.assertEqual(self.test.question.first().question,
                         'Question')
        self.assertEqual(self.test.question.first().answer.answer,
                         'Answer1')

    def test_str_representation(self):
        expected_str = 'Вопрос: Question, Дата создания: 2023-01-01T00:00:00Z'
        self.assertEqual(str(self.test), expected_str)

    def test_constraint(self):
        # Проверка даты обновления позже или с одинаковой с датой создания
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Test.objects.create(
                    creation_date=timezone.now(),
                    last_update=timezone.now() - timedelta(days=1),
                )

    def test_clean_method(self):
        # Проверка даты обновления позже или с одинаковой с датой создания
        with self.assertRaises(IntegrityError):
            with self.assertRaises(ValidationError):
                with transaction.atomic():
                    test = Test.objects.create(
                        creation_date=timezone.now(),
                        last_update=timezone.now() - timedelta(days=1),
                    )
                    test.clean()
        test = Test.objects.create(
            creation_date=timezone.now(),
            last_update=timezone.now(),
        )
        test.clean()
        test = Test.objects.create(
            creation_date=timezone.now() - timedelta(days=1),
            last_update=timezone.now(),
        )
        test.clean()

    def test_save_method(self):
        test = Test.objects.create()
        # Автозапись даты создания
        self.assertEqual(test.creation_date.date(), timezone.now().date())
        # Автозапись даты обновления
        self.assertEqual(test.last_update.date(), timezone.now().date())
