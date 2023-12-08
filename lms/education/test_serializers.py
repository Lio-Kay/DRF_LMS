from django.test import TestCase
from django.utils import timezone

from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion)
from education.serializers import (MediaLinkSerializer,
                                   MaterialListSerializer, MaterialRetrieveSerializer,
                                   SectionListSerializer, SectionRetrieveSerializer,
                                   TestAnswerSerializer, TestQuestionSerializer)


class MediaLinkSerializerTest(TestCase):

    maxDiff = None

    def setUp(self):
        self.media = Media.objects.create(
            local_image='/image.jpg',
            external_image='https://example.com/image.jpg',
            local_video='/video.mp4',
            external_video='https://example.com/video.mp4',
            local_audio='/audio.mp3',
            external_audio='https://example.com/audio.mp3',
        )

    def tearDown(self):
        self.media.delete()

    def test_to_representation(self):
        serializer = MediaLinkSerializer(instance=self.media)
        expected_data = {
            'local_image': '/image.jpg',
            'external_image': 'https://example.com/image.jpg',
            'local_video': '/video.mp4',
            'external_video': 'https://example.com/video.mp4',
            'local_audio': '/audio.mp3',
            'external_audio': 'https://example.com/audio.mp3',
        }
        self.assertEqual(serializer.data, expected_data)

    def test_meta_fields(self):
        serializer = MediaLinkSerializer()
        expected_fields = ('local_image', 'external_image',
                           'local_video', 'external_video',
                           'local_audio', 'external_audio',)
        self.assertEqual(serializer.Meta.model, Media)
        self.assertEqual(serializer.Meta.fields, expected_fields)


class MaterialListSerializerTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(name='Section_1')
        self.media = Media.objects.create(name='Media_1')
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

    def test_get_media_names(self):
        serializer = MaterialListSerializer(instance=self.material)
        expected_media_name = 'Media_1'
        self.assertEqual(serializer.data['media_names'], expected_media_name)

    def test_meta_fields(self):
        serializer = MaterialListSerializer()
        expected_fields = ('name', 'section', 'status',
                           'creation_date', 'last_update',
                           'media_names', 'media_links',)
        self.assertEqual(serializer.Meta.model, Material)
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_media_links_serializer(self):
        serializer = MaterialListSerializer(instance=self.material)
        media_links_serializer = MediaLinkSerializer(instance=self.material.media.all(), many=True)
        expected_media_links = media_links_serializer.data
        self.assertEqual(serializer.data['media_links'], expected_media_links)


class MaterialRetrieveSerializerTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(name='Section_1')
        self.media = Media.objects.create(name='Media_1')
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

    def test_get_media_names(self):
        serializer = MaterialRetrieveSerializer(instance=self.material)
        expected_media_name = 'Media_1'
        self.assertEqual(serializer.data['media_names'], expected_media_name)

    def test_meta_fields(self):
        serializer = MaterialRetrieveSerializer()
        expected_fields = ('name', 'section', 'status', 'text',
                           'creation_date', 'last_update',
                           'media_names', 'media_links',)
        self.assertEqual(serializer.Meta.model, Material)
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_media_links_serializer(self):
        serializer = MaterialRetrieveSerializer(instance=self.material)
        media_links_serializer = MediaLinkSerializer(instance=self.material.media.all(), many=True)
        expected_media_links = media_links_serializer.data
        self.assertEqual(serializer.data['media_links'], expected_media_links)


class SectionListSerializerTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(name='Section_1', base_price=10)
        self.media = Media.objects.create(name='Media_1')
        self.material = Material.objects.create(name='Material_1', section=self.section)
        self.section.media.add(self.media)

    def tearDown(self):
        self.section.delete()
        self.media.delete()
        self.material.delete()

    def test_get_media_names(self):
        serializer = SectionListSerializer(instance=self.section)
        expected_media_names = ['Media_1']
        self.assertEqual(list(serializer.data['media_names']), expected_media_names)

    def test_meta_fields(self):
        serializer = SectionListSerializer()
        expected_fields = ('name', 'status', 'creation_date', 'last_update',
                           'materials_count', 'base_price',
                           'media_names', 'media_links',)
        self.assertEqual(serializer.Meta.model, Section)
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_media_links_serializer(self):
        serializer = SectionListSerializer(instance=self.section)
        media_links_serializer = MediaLinkSerializer(
            instance=self.section.media.all(), many=True)
        expected_media_links = media_links_serializer.data
        self.assertEqual(serializer.data['media_links'], expected_media_links)
