from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from django.db.utils import IntegrityError
from datetime import timedelta

from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion, Test)


class MediaModelTests(TestCase):
    def setUp(self):
        self.media = Media.objects.create(
            name='Test_Media',
            external_image='https://placehold.co/600x400/EEE/31343C'
        )

    def tearDown(self):
        self.media.delete()

    def test_create_media(self):
        media_count = Media.objects.count()
        self.assertEqual(media_count, 1)
        self.assertEqual(self.media.name, 'Test_Media')
        self.assertEqual(self.media.external_image, 'https://placehold.co/600x400/EEE/31343C')

    def test_one_media_selected(self):
        media = Media(name='Test_Media')
        with self.assertRaises(ValidationError):
            media.clean()

# Create your tests here.
        media.local_image = 'path/to/image.jpg'
        media.external_video = 'https://example.com/video.mp4'
        with self.assertRaises(ValidationError):
            media.clean()

        media.local_image = ''
        media.external_image = 'https://example.com/image.jpg'
        with self.assertRaises(ValidationError):
            media.clean()

        media.external_image = ''
        media.local_video = 'path/to/video.mp4'
        with self.assertRaises(ValidationError):
            media.clean()

        media.local_video = ''
        media.external_audio = 'https://example.com/audio.mp3'
        with self.assertRaises(ValidationError):
            media.clean()

        media.external_audio = ''
        media.external_video = ''
        media.local_audio = 'path/to/audio.mp3'
        media.clean()

    def test_creation_date_auto_set(self):
        media = Media.objects.create(name='Test_Media')
        self.assertIsNotNone(media.creation_date)
        self.assertEqual(media.creation_date.date(), timezone.now().date())

