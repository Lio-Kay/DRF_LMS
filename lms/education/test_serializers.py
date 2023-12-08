from django.test import TestCase
from education.models import Media
from education.serializers import MediaLinkSerializer


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
