from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from education.serializers import (SectionListSerializer, SectionRetrieveSerializer,
                                   MaterialListSerializer, MaterialRetrieveSerializer,
                                   TestQuestionSerializer)
from education.models import Section, Material, Test


class SectionsListAPIView(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionListSerializer


class SectionsRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionRetrieveSerializer


class MaterialsListAPIView(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialListSerializer


class MaterialsRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialRetrieveSerializer


class StartTest(APIView):

    def get(self, request, pk):
        try:
            test = Test.objects.get(material__pk=pk)
        except Test.DoesNotExist:
            raise Http404
        serializer = TestQuestionSerializer(test.question.all(), many=True)
        print(serializer.data)
        return Response(serializer.data)
