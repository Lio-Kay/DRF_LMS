from django.urls import path

from education.apps import EducationConfig
from education.views import (SectionsListAPIView, SectionsRetrieveAPIView,
                             MaterialListSerializer, MaterialRetrieveSerializer,
                             StartTest)


app_name = EducationConfig.name

urlpatterns = [
    path('sections/', SectionsListAPIView.as_view(), name='sections_list'),
    path('section/<int:pk>/ ', SectionsRetrieveAPIView.as_view(), name='section_detail'),
    path('materials/ ', MaterialListSerializer.as_view(), name='materials_list'),
    path('material/<int:pk>/ ', MaterialRetrieveSerializer.as_view(), name='material_detail'),
    path('material/<int:pk>/test/ ', StartTest.as_view(), name='material_test'),
]
