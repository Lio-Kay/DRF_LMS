from django.contrib import admin

from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion, Test)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creation_date', 'local_image',
                    'external_image', 'local_video', 'external_video',
                    'local_audio', 'external_audio',)
    list_display_links = ('id', 'creation_date', 'local_image',
                          'external_image', 'local_video', 'external_video',
                          'local_audio', 'external_audio',)
    search_fields = 'name', 'creation_date',
    list_editable = 'name',


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'creation_date', 'last_update',
                    'base_price',)
    list_display_links = ('id', 'creation_date', 'last_update',)
    list_filter = 'status',
    search_fields = 'name', 'creation_date', 'last_update',
    list_editable = 'name', 'status', 'base_price',


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'creation_date', 'last_update',
                    'section',)
    list_display_links = ('id', 'creation_date', 'last_update', 'section',)
    list_filter = 'status', 'section',
    search_fields = 'name', 'creation_date', 'last_update',
    list_editable = 'name', 'status',


@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    list_display = 'id', 'answer',
    list_display_links = 'id',
    list_editable = 'answer',


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = 'id', 'question', 'answer', 'media',
    list_display_links = 'id', 'question', 'answer', 'media',
    search_fields = 'question',


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = 'id', 'material', 'creation_date', 'last_update',
    list_display_links = 'id', 'material', 'creation_date', 'last_update',
    search_fields = 'material', 'creation_date', 'last_update',
