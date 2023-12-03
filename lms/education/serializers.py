from rest_framework import serializers

from education.models import Section, Material, TestAnswer, TestQuestion


class MaterialListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = 'name', 'section', 'media',


class MaterialRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = 'name', 'section', 'text', 'last_update', 'media',


class SectionListSerializer(serializers.ModelSerializer):
    materials_count = serializers.IntegerField(source='material_section.all.count')

    class Meta:
        model = Section
        fields = 'name', 'last_update', 'materials_count', 'base_price', 'media',


class SectionRetrieveSerializer(serializers.ModelSerializer):
    materials_count = serializers.IntegerField(source='material_section.all.count')
    materials = MaterialListSerializer(source='material_section', many=True, read_only=True)

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
        ordered_queryset = TestAnswer.objects.filter(testquestion_choices__pk=obj.pk).order_by('?')
        return TestAnswerSerializer(ordered_queryset, many=True, context=self.context).data

    class Meta:
        model = TestQuestion
        fields = 'question', 'choices',
