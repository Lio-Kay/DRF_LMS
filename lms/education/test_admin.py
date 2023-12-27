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
        self.section = Section.objects.create(name='Test_Section')

    def test_set_last_update_now(self):
        queryset = Section.objects.filter(pk=self.section.pk)
        set_last_update_now(None, None, queryset)
        self.section.refresh_from_db()
        self.assertAlmostEqual(self.section.last_update, timezone.now(),
                               delta=timezone.timedelta(seconds=1))

    def test_set_archived_status(self):
        self.section.status = 'OPEN'
        queryset = Section.objects.filter(pk=self.section.pk)
        set_archived_status(None, None, queryset)
        self.section.refresh_from_db()
        self.assertEqual(self.section.status, 'ARCHIVED')

    def test_set_closed_status(self):
        self.section.status = 'OPEN'
        queryset = Section.objects.filter(pk=self.section.pk)
        set_closed_status(None, None, queryset)
        self.section.refresh_from_db()
        self.assertEqual(self.section.status, 'CLOSED')

    def test_set_open_status(self):
        self.section.status = 'CLOSED'
        queryset = Section.objects.filter(pk=self.section.pk)
        set_open_status(None, None, queryset)
        self.section.refresh_from_db()
        self.assertEqual(self.section.status, 'OPEN')

        self.assertEqual(section.status, 'OPEN')
