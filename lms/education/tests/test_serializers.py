from django.test import TestCase
from django.utils import timezone

from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion)
from education.serializers import (MediaLinkSerializer,
                                   MaterialListSerializer,
                                   MaterialRetrieveSerializer,
                                   SectionListSerializer,
                                   SectionRetrieveSerializer,
                                   TestAnswerSerializer,
                                   TestQuestionSerializer)


class MediaLinkSerializerTest(TestCase):

    maxDiff = None

    def setUp(self):
        self.media = Media.objects.create(
            pk=1,
            name='Test_Media',
            local_audio='/audio.mp3',
        )

    def tearDown(self):
        self.media.delete()

    def test_to_representation(self):
        serializer = MediaLinkSerializer(instance=self.media)
        expected_data = {
            'pk': 1,
            'name': 'Test_Media',
            'local_audio': '/audio.mp3',
        }
        self.assertEqual(serializer.data, expected_data)

    def test_meta_fields(self):
        serializer = MediaLinkSerializer()
        expected_fields = ('pk', 'name',
                           'local_image', 'external_image',
                           'local_video', 'external_video',
                           'local_audio', 'external_audio',)
        self.assertEqual(serializer.Meta.model, Media)
        self.assertEqual(serializer.Meta.fields, expected_fields)


class MaterialListSerializerTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(
            name='Section_1')
        self.media = Media.objects.create(
            name='Media_1',
            local_image='path/to/image.jpg')
        self.material = Material.objects.create(
            name='Material_1',
            section=self.section,
            status='OPEN',
            creation_date=timezone.now(),
            last_update=timezone.now(),
        )
        self.material.media.add(self.media)

    def tearDown(self):
        self.section.delete()
        self.media.delete()
        self.material.delete()

    def test_get_section(self):
        serializer = MaterialListSerializer(instance=self.material)
        expected_section = 'Section_1'
        self.assertEqual(serializer.data['section'], expected_section)

    def test_meta_fields(self):
        serializer = MaterialListSerializer()
        expected_fields = ('pk', 'name', 'section', 'status',
                           'creation_date', 'last_update',
                           'media_links',)
        self.assertEqual(serializer.Meta.model, Material)
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_media_links_serializer(self):
        serializer = MaterialListSerializer(instance=self.material)
        media_links_serializer = MediaLinkSerializer(
            instance=self.material.media.all(), many=True)
        expected_media_links = media_links_serializer.data
        self.assertEqual(serializer.data['media_links'], expected_media_links)


class MaterialRetrieveSerializerTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(
            name='Section_1')
        self.media = Media.objects.create(
            name='Media_1',
            local_image='path/to/image.jpg')
        self.material = Material.objects.create(
            name='Material_1',
            section=self.section,
            status='OPEN',
            text='Lorem ipsum dolor sit amet.',
            creation_date=timezone.now(),
            last_update=timezone.now(),
        )
        self.material.media.add(self.media)

    def tearDown(self):
        self.section.delete()
        self.media.delete()
        self.material.delete()

    def test_get_section(self):
        serializer = MaterialRetrieveSerializer(instance=self.material)
        expected_section = 'Section_1'
        self.assertEqual(serializer.data['section'], expected_section)

    def test_meta_fields(self):
        serializer = MaterialRetrieveSerializer()
        expected_fields = ('pk', 'name', 'section', 'status', 'text',
                           'creation_date', 'last_update',
                           'media_links',)
        self.assertEqual(serializer.Meta.model, Material)
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_media_links_serializer(self):
        serializer = MaterialRetrieveSerializer(instance=self.material)
        media_links_serializer = MediaLinkSerializer(
            instance=self.material.media.all(), many=True)
        expected_media_links = media_links_serializer.data
        self.assertEqual(serializer.data['media_links'], expected_media_links)


class SectionListSerializerTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(
            name='Section_1',
            base_price=10)
        self.media = Media.objects.create(
            name='Media_1',
            local_image='path/to/image.jpg')
        self.material = Material.objects.create(
            name='Material_1',
            section=self.section)
        self.section.media.add(self.media)

    def tearDown(self):
        self.section.delete()
        self.media.delete()
        self.material.delete()

    def test_meta_fields(self):
        serializer = SectionListSerializer()
        expected_fields = ('pk', 'name', 'status',
                           'creation_date', 'last_update',
                           'materials_count', 'base_price',
                           'media_links',)
        self.assertEqual(serializer.Meta.model, Section)
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_media_links_serializer(self):
        serializer = MaterialRetrieveSerializer(instance=self.material)
        media_links_serializer = MediaLinkSerializer(
            instance=self.material.media.all(), many=True)
        expected_media_links = media_links_serializer.data
        self.assertEqual(serializer.data['media_links'], expected_media_links)


class SectionRetrieveSerializerTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(
            name='Section_1',
            status='OPEN',
            description='Section description',
            base_price=10.99
        )
        self.material1 = Material.objects.create(
            name='Material_1',
            section=self.section,
            status='OPEN',
            text='Lorem ipsum dolor sit amet.'
        )
        self.material2 = Material.objects.create(
            name='Material_2',
            section=self.section,
            status='OPEN',
            text='Lorem ipsum dolor sit amet.'
        )
        self.media1 = Media.objects.create(
            name='Media_1',
            local_image='path/to/image2.jpg')
        self.media2 = Media.objects.create(
            name='Media_2',
            local_image='path/to/image2.jpg')
        self.section.media.add(self.media1, self.media2)

    def tearDown(self):
        self.section.delete()
        self.media1.delete()
        self.media2.delete()
        self.material1.delete()
        self.material2.delete()

    def test_get_materials_names(self):
        serializer = SectionRetrieveSerializer(instance=self.section)
        materials_names = serializer.data['materials']
        expected_materials_names = ['Material_1', 'Material_2']
        self.assertEqual(list(materials_names), expected_materials_names)

    def test_meta_fields(self):
        serializer = SectionRetrieveSerializer()
        expected_fields = ('pk', 'name', 'status', 'description',
                           'creation_date', 'last_update',
                           'base_price', 'materials',
                           'media_links',)
        self.assertEqual(serializer.Meta.model, Section)
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_media_links_serializer(self):
        serializer = SectionRetrieveSerializer(instance=self.section)
        media_links = serializer.data['media_links']
        self.assertEqual(len(media_links), 2)
        media_links_serializer = MediaLinkSerializer(
            instance=self.section.media.all(), many=True)
        expected_media_links = media_links_serializer.data
        self.assertEqual(serializer.data['media_links'], expected_media_links)


class TestAnswerSerializerTest(TestCase):
    def setUp(self):
        self.test_answer = TestAnswer.objects.create(
            pk=1,
            answer='Answer'
        )

    def tearDown(self):
        self.test_answer.delete()

    def test_meta_fields(self):
        serializer = TestAnswerSerializer()
        expected_fields = ('pk', 'answer',)
        self.assertEqual(serializer.Meta.model, TestAnswer)
        self.assertEqual(serializer.Meta.fields, expected_fields)


class TestQuestionSerializerTest(TestCase):
    def setUp(self):
        self.test_answer1 = TestAnswer.objects.create(answer='Answer_1')
        self.test_answer2 = TestAnswer.objects.create(answer='Answer_2')
        self.test_question = TestQuestion.objects.create(
            question='Question',
            answer=self.test_answer1)
        self.test_question.choices.add(self.test_answer1, self.test_answer2)

    def tearDown(self):
        self.test_answer1.delete()
        self.test_answer2.delete()
        self.test_question.delete()

    def test_get_choices(self):
        serializer = TestQuestionSerializer(instance=self.test_question)
        expected_choices = TestAnswer.objects.filter(
            testquestion_choices=self.test_question).order_by('answer')
        choices_data = serializer.get_choices(self.test_question)
        sorted_choices_data = sorted(choices_data, key=lambda x: x['answer'])
        self.assertEqual(sorted_choices_data, TestAnswerSerializer(
            expected_choices, many=True).data)

    def test_meta_fields(self):
        serializer = TestQuestionSerializer()
        expected_fields = ('pk', 'question', 'choices',)
        self.assertEqual(serializer.Meta.model, TestQuestion)
        self.assertEqual(serializer.Meta.fields, expected_fields)
