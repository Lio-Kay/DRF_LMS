from django.urls import path

from education.apps import EducationConfig
from education.views import (SectionsListAPIView, SectionsRetrieveAPIView,
                             MaterialsListAPIView, MaterialsRetrieveAPIView,
                             StartTest)


app_name = EducationConfig.name

urlpatterns = [
    path('sections/', SectionsListAPIView.as_view(),
         name='sections_list'),
    path('sections/<int:pk>/', SectionsRetrieveAPIView.as_view(),
         name='section_detail'),
    path('materials/', MaterialsListAPIView.as_view(),
         name='materials_list'),
    path('materials/<int:pk>/', MaterialsRetrieveAPIView.as_view(),
         name='material_detail'),
    path('materials/<int:pk>/test/', StartTest.as_view(),
         name='material_test'),
]
