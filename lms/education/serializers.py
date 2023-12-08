from rest_framework import serializers

from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion)


class MediaLinkSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None}

    class Meta:
        model = Media
        fields = ('local_image', 'external_image',
                  'local_video', 'external_video',
                  'local_audio', 'external_audio',)


class MaterialListSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField('get_section')
    media_name = serializers.SerializerMethodField('get_media_name')
    media_link = MediaLinkSerializer(source='media', many=True)

    def get_section(self, obj):
        return obj.section.name

    def get_media_name(self, obj):
        media_names = obj.media.values_list('name', flat=True)
        return media_names[0]

    class Meta:
        model = Material
        fields = ('name', 'section', 'status',
                  'creation_date', 'last_update',
                  'media_name', 'media_link',)


class MaterialRetrieveSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField('get_section')
    media_name = serializers.SerializerMethodField('get_media_name')
    media_link = MediaLinkSerializer(source='media', many=True)

    def get_section(self, obj):
        return obj.section.name

    def get_media_name(self, obj):
        media_name = obj.media.values_list('name', flat=True)
        return media_name[0]

    class Meta:
        model = Material
        fields = ('name', 'section', 'status', 'text',
                  'creation_date', 'last_update',
                  'media_name', 'media_link',)


class SectionListSerializer(serializers.ModelSerializer):
    materials_count = serializers.IntegerField(source='material_section.all.count')

    class Meta:
        model = Section
        fields = ('name', 'last_update', 'materials_count', 'base_price',
                  'media',)


class SectionRetrieveSerializer(serializers.ModelSerializer):
    materials_count = serializers.IntegerField(source='material_section.all.count')
    materials = MaterialListSerializer(source='material_section',
                                       many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('name', 'last_update', 'materials_count', 'base_price',
                  'description', 'materials', 'media',)


class TestAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestAnswer
        fields = 'pk', 'answer',


class TestQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    def get_choices(self, obj):
        ordered_queryset = TestAnswer.objects.filter(
            testquestion_choices__pk=obj.pk).order_by('?')
        return TestAnswerSerializer(ordered_queryset,
                                    many=True, context=self.context).data

    class Meta:
        model = TestQuestion
        fields = 'question', 'choices',
