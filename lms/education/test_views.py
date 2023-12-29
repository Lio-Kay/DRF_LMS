from collections import OrderedDict

from django.test import TestCase
from django.urls import reverse
from rest_framework import status, test

from education.models import Test, Material, TestQuestion, TestAnswer
from education.serializers import TestQuestionSerializer


class StartTestAPIViewTest(TestCase):
    def setUp(self):
        self.client = test.APIClient()
        self.material = Material.objects.create(name='Test_Material')
        self.answer1 = TestAnswer.objects.create(answer='Answer_1')
        self.answer2 = TestAnswer.objects.create(answer='Answer_2')
        self.answer3 = TestAnswer.objects.create(answer='Answer_3')
        self.question1 = TestQuestion.objects.create(
            question='Question_1',
            answer=self.answer1)
        self.question2 = TestQuestion.objects.create(
            question='Question_2',
            answer=self.answer3)
        self.question1.choices.add(self.answer1, self.answer2)
        self.question2.choices.add(self.answer2, self.answer3)
        self.test = Test.objects.create(
            material=self.material)
        self.test.question.add(self.question1, self.question2)

    def tearDown(self):
        self.material.delete()
        self.answer1.delete()
        self.answer2.delete()
        self.answer3.delete()
        self.question1.delete()
        self.question2.delete()
        self.test.delete()

    def test_start_test_get_existing_test(self):
        url = reverse('education:material_test',
                      kwargs={'pk': self.material.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = TestQuestionSerializer(
            [self.question1, self.question2], many=True)
        sorted_serializer_data = [
            OrderedDict([
                ('question', d['question']),
                ('choices', sorted(d['choices'], key=lambda c: c['pk']))
            ])
            for d in serializer.data
        ]
        sorted_response_data = [
            OrderedDict([
                ('question', d['question']),
                ('choices', sorted(d['choices'], key=lambda c: c['pk']))
            ])
            for d in response.data
        ]
        self.assertEqual(sorted_response_data, sorted_serializer_data)

    def test_start_test_get_nonexistent_test(self):
        url = reverse('education:material_test', kwargs={'pk': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
