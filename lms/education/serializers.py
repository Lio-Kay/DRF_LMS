from rest_framework import serializers

from education.models import (Media, Section, Material, TestAnswer,
                              TestQuestion)


class MediaLinkSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None}

    class Meta:
        model = Media
        fields = ('pk', 'name',
                  'local_image', 'external_image',
                  'local_video', 'external_video',
                  'local_audio', 'external_audio',)


class MaterialListSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField('get_section')
    media_links = MediaLinkSerializer(source='media', many=True)

    def get_section(self, obj):
        return obj.section.name

    class Meta:
        model = Material
        fields = ('pk', 'name', 'section', 'status',
                  'creation_date', 'last_update',
                  'media_links',)


class MaterialRetrieveSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField('get_section')
    media_links = MediaLinkSerializer(source='media', many=True)

    def get_section(self, obj):
        return obj.section.name

    class Meta:
        model = Material
        fields = ('pk', 'name', 'section', 'status', 'text',
                  'creation_date', 'last_update',
                  'media_links',)


class SectionListSerializer(serializers.ModelSerializer):
    materials_count = serializers.IntegerField(
        source='material_section.all.count')
    media_links = MediaLinkSerializer(source='media', many=True)

    class Meta:
        model = Section
        fields = ('pk', 'name', 'status', 'creation_date', 'last_update',
                  'materials_count', 'base_price',
                  'media_links',)


class SectionRetrieveSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField('get_materials_names')
    media_links = MediaLinkSerializer(source='media', many=True)

    def get_materials_names(self, obj):
        materials_names = obj.material_section.values_list('name', flat=True)
        return materials_names

    class Meta:
        model = Section
        fields = ('pk', 'name', 'status', 'description',
                  'creation_date', 'last_update', 'base_price',
                  'materials', 'media_links',)


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
        fields = 'pk', 'question', 'choices',
