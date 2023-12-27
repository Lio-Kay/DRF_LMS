from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

from education.admin import (SectionAdmin, MaterialAdmin, set_last_update_now,
                             set_archived_status, set_closed_status,
                             set_open_status)
from education.models import Section, Material


User = get_user_model()


class AdminActionsTests(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.section_admin = SectionAdmin(Section, self.admin_site)

    def test_set_last_update_now(self):
        section = Section.objects.create(name='Test Section')
        queryset = Section.objects.filter(pk=section.pk)

        set_last_update_now(None, None, queryset)
        section.refresh_from_db()

        self.assertAlmostEqual(section.last_update, timezone.now(),
                               delta=timezone.timedelta(seconds=1))

    def test_set_archived_status(self):
        section = Section.objects.create(name='Test Section',
                                         status='OPEN')
        queryset = Section.objects.filter(pk=section.pk)

        set_archived_status(None, None, queryset)
        section.refresh_from_db()

        self.assertEqual(section.status, 'ARCHIVED')

    def test_set_closed_status(self):
        section = Section.objects.create(name='Test Section',
                                         status='OPEN')
        queryset = Section.objects.filter(pk=section.pk)

        set_closed_status(None, None, queryset)
        section.refresh_from_db()

        self.assertEqual(section.status, 'CLOSED')

    def test_set_open_status(self):
        section = Section.objects.create(name='Test Section',
                                         status='CLOSED')
        queryset = Section.objects.filter(pk=section.pk)

        set_open_status(None, None, queryset)
        section.refresh_from_db()

        self.assertEqual(section.status, 'OPEN')
