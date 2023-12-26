from django.contrib import admin
from django.utils import timezone
from django.urls import reverse
from django.utils.safestring import mark_safe

from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion, Test)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    fields = ('name', 'creation_date',
              ('local_image', 'external_image'),
              ('local_video', 'external_video'),
              ('local_audio', 'external_audio'),)
    list_display = ('id', 'name', 'creation_date', 'local_image',
                    'external_image', 'local_video', 'external_video',
                    'local_audio', 'external_audio',)
    list_display_links = ('id', 'creation_date', 'local_image',
                          'external_image', 'local_video', 'external_video',
                          'local_audio', 'external_audio',)
    search_fields = 'name', 'creation_date',
    list_editable = 'name',


@admin.action(description='Обновить выбранные элементы')
def set_last_update_now(modeladmin, request, queryset):
    queryset.update(last_update=timezone.now())


@admin.action(description='Архивировать выбранные элементы')
def set_archived_status(modeladmin, request, queryset):
    queryset.update(status='ARCHIVED')


@admin.action(description='Закрыть выбранные элементы')
def set_closed_status(modeladmin, request, queryset):
    queryset.update(status='CLOSED')


@admin.action(description='Открыть выбранные элементы')
def set_open_status(modeladmin, request, queryset):
    queryset.update(status='OPEN')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    fields = (('name', 'status'),
              'description',
              ('creation_date', 'last_update'),
              'base_price', 'media',)
    list_display = ('id', 'name', 'status', 'creation_date', 'last_update',
                    'base_price',)
    list_display_links = ('id', 'creation_date', 'last_update',)
    list_filter = 'status',
    search_fields = 'name', 'creation_date', 'last_update',
    list_editable = 'name', 'status', 'base_price',
    actions = (set_last_update_now, set_archived_status, set_closed_status,
               set_open_status)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    fields = (('name', 'status'),
              'section', 'text',
              ('creation_date', 'last_update'),
              'media', )
    list_display = ('id', 'name', 'status', 'creation_date', 'last_update',
                    'section_link',)
    list_display_links = ('id', 'creation_date', 'last_update',)
    list_filter = 'status', 'section',
    search_fields = 'name', 'creation_date', 'last_update',
    list_editable = 'name', 'status',
    actions = (set_last_update_now, set_archived_status, set_closed_status,
               set_open_status)

    def section_link(self, obj):
        try:
            link = mark_safe('<a href="{}">{}</a>'.format(
                reverse('admin:education_section_change',
                        args=(obj.section.pk,)), obj.section.name))
        except AttributeError:
            link = ''
        return link

    section_link.short_description = 'Раздел'


@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    list_display = 'id', 'answer',
    list_display_links = 'id',
    list_editable = 'answer',


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    fields = 'question', ('answer', 'choices'), 'media',
    list_display = 'id', 'question', 'answer', 'media',
    list_display_links = 'id', 'question', 'answer', 'media',
    search_fields = 'question',


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    fields = 'material', 'question', ('creation_date', 'last_update'),
    list_display = 'id', 'material', 'creation_date', 'last_update',
    list_display_links = 'id', 'material', 'creation_date', 'last_update',
    search_fields = 'material', 'creation_date', 'last_update',
    actions = set_last_update_now,
