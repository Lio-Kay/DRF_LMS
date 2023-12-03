from django.db import models
from djmoney.models.fields import MoneyField

from education.apps import EducationConfig


app_name = EducationConfig.name

NULLABLE = {'blank': True, 'null': True}


class Media(models.Model):
    """Модель медиа"""
    name = models.CharField(max_length=100, verbose_name='Название')

    creation_date = models.DateTimeField(**NULLABLE, verbose_name='Дата создания')

    local_image = models.ImageField(**NULLABLE, upload_to='education/media/images/%Y/%m/%d/',
                                    verbose_name='Локальное изображение')
    external_image = models.URLField(**NULLABLE, verbose_name='Внешнее изображение')
    local_video = models.FileField(**NULLABLE, upload_to='education/media/videos/%Y/%m/%d/',
                                   verbose_name='Локальное видео')
    external_video = models.URLField(**NULLABLE, verbose_name='Внешнее видео')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'медиа'
        verbose_name_plural = 'медиа'
        ordering = 'name',


class Section(models.Model):
    """Модель раздела"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    status_choices = [
        ('ARCHIVED', 'Архивированный'),
        ('CLOSED', 'Закрытый'),
        ('OPEN', 'Открытый'),
    ]
    status = models.CharField(**NULLABLE, max_length=8, choices=status_choices, default='CLOSED',
                              verbose_name='Статус раздела')

    creation_date = models.DateTimeField(**NULLABLE, verbose_name='Дата создания')
    last_update = models.DateTimeField(**NULLABLE, verbose_name='Дата последнего обновления')

    base_price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB', verbose_name='Базовая цена')

    media = models.ManyToManyField(to=Media, related_name='section_media')

    def __str__(self):
        return f'{self.name}, {self.status}, {self.creation_date}'

    class Meta:
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'
        ordering = 'name',


class Material(models.Model):
    """Модель материала"""
    name = models.CharField(max_length=100, verbose_name='Название')
    text = models.TextField(**NULLABLE, verbose_name='Текст')
    status_choices = [
        ('ARCHIVED', 'Архивированный'),
        ('CLOSED', 'Закрытый'),
        ('OPEN', 'Открытый'),
    ]
    status = models.CharField(**NULLABLE, max_length=8, choices=status_choices, default='CLOSED',
                              verbose_name='Статус материала')

    creation_date = models.DateTimeField(**NULLABLE, verbose_name='Дата создания')
    last_update = models.DateTimeField(**NULLABLE, verbose_name='Дата последнего обновления')

    media = models.ManyToManyField(to=Media, related_name='material_media')
    section = models.ForeignKey(**NULLABLE, to=Section, on_delete=models.SET_NULL, related_name='material_section')

    def __str__(self):
        return f'{self.name}, {self.status}, {self.creation_date}'

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
        ordering = 'name',


class Test(models.Model):
    """Модель теста"""
    material = models.OneToOneField(**NULLABLE, to=Material, on_delete=models.CASCADE,
                                    related_name='test_material')
    question = models.ManyToManyField(to=MaterialQuestion, related_name='test_question')

    creation_date = models.DateTimeField(**NULLABLE, verbose_name='Дата создания')
    last_update = models.DateTimeField(**NULLABLE, verbose_name='Дата последнего обновления')

    def __str__(self):
        return f'{self.material}, {self.question}'

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'
        ordering = 'material',


class TestQuestion(models.Model):
    """Модель вопроса теста"""
    question = models.TextField(verbose_name='Вопрос')
    media = models.ManyToManyField(to=Media, related_name='testquestion_media')

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'
        ordering = 'name',
