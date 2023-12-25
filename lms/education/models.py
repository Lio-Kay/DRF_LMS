from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from djmoney.models.fields import MoneyField

from education.apps import EducationConfig

app_name = EducationConfig.name

NULLABLE = {'blank': True, 'null': True}


class Media(models.Model):
    """Модель медиа"""
    name = models.CharField(
        max_length=100, verbose_name='Название')

    creation_date = models.DateTimeField(
        **NULLABLE, verbose_name='Дата создания')

    local_image = models.ImageField(
        **NULLABLE, upload_to='education/media/images/%Y/%m%d/',
        verbose_name='Локальное изображение')
    external_image = models.URLField(
        **NULLABLE, verbose_name='Внешнее изображение')
    local_video = models.FileField(
        **NULLABLE, upload_to='education/media/videos/%Y/%m%d/',
        verbose_name='Локальное видео')
    external_video = models.URLField(
        **NULLABLE, verbose_name='Внешнее видео')
    local_audio = models.FileField(
        **NULLABLE, upload_to='education/media/audios/%Y/%m%d/',
        verbose_name='Локальное аудио')
    external_audio = models.URLField(
        **NULLABLE, verbose_name='Внешнее аудио')

    def __str__(self):
        fields = [self.name]
        if self.creation_date:
            fields.append(str(self.creation_date))
        if self.local_image:
            fields.append(str(self.local_image))
        if self.external_image:
            fields.append(self.external_image)
        if self.local_video:
            fields.append(str(self.local_video))
        if self.external_video:
            fields.append(self.external_video)
        if self.local_audio:
            fields.append(str(self.local_audio))
        if self.external_audio:
            fields.append(self.external_audio)

        return ', '.join(fields)

    class Meta:
        verbose_name = 'медиа'
        verbose_name_plural = 'медиа'
        ordering = 'name',

    def clean(self):
        # Проверка на обязательный выбор только одного медиа файла
        image_fields = [self.local_image, self.external_image]
        video_fields = [self.local_video, self.external_video]
        audio_fields = [self.local_audio, self.external_audio]

        if not any(image_fields) and not any(video_fields) and not any(
                audio_fields):
            raise ValidationError('Медиа файл должен быть указан')
        if sum(bool(field) for field in image_fields) + sum(
                bool(field) for field in video_fields) + sum(
            bool(field) for field in audio_fields) > 1:
            raise ValidationError('Только один медиа файл может быть выбран')

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None, *args, **kwargs):
        # Автозапись даты создания
        if not self.creation_date:
            self.creation_date = timezone.now()
        super().save(force_insert, force_update, using, update_fields,
                     *args, **kwargs)


class Section(models.Model):
    """Модель раздела"""
    name = models.CharField(
        max_length=100, verbose_name='Название')
    description = models.TextField(
        verbose_name='Описание')
    status_choices = [
        ('ARCHIVED', 'Архивированный'),
        ('CLOSED', 'Закрытый'),
        ('OPEN', 'Открытый'),
    ]
    status = models.CharField(
        **NULLABLE, max_length=8, choices=status_choices, default='CLOSED',
        verbose_name='Статус раздела')

    creation_date = models.DateTimeField(
        **NULLABLE, verbose_name='Дата создания')
    last_update = models.DateTimeField(
        **NULLABLE, verbose_name='Дата последнего обновления')

    base_price = MoneyField(
        max_digits=14, decimal_places=2, default=0, default_currency='RUB',
        verbose_name='Базовая цена')

    media = models.ManyToManyField(
        blank=True, to=Media, related_name='section_media')

    def __str__(self):
        return (f'Name: {self.name}, Status: {self.status}, '
                f'Created: {self.creation_date}, '
                f'Base price: {self.base_price}')

    class Meta:
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'
        ordering = 'name',
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_last_update_after_creation_date',
                check=models.Q(last_update__gte=models.F('creation_date')),
            )
        ]

    def clean(self):
        # Проверка даты обновления позже или одинаковой с датой создания
        if self.last_update < self.creation_date:
            raise models.ValidationError(
                'Дата обновления не может быть раньше даты создания'
            )

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None, *args, **kwargs):
        # Автозапись даты создания
        if not self.creation_date:
            self.creation_date = timezone.now()
        # Автозапись даты обновления
        if not self.last_update:
            self.last_update = timezone.now()
        super().save(force_insert, force_update, using, update_fields,
                     *args, **kwargs)


class Material(models.Model):
    """Модель материала"""
    name = models.CharField(
        max_length=100, verbose_name='Название')
    text = models.TextField(
        **NULLABLE, verbose_name='Текст')
    status_choices = [
        ('ARCHIVED', 'Архивированный'),
        ('CLOSED', 'Закрытый'),
        ('OPEN', 'Открытый'),
    ]
    status = models.CharField(
        **NULLABLE, max_length=8, choices=status_choices, default='CLOSED',
        verbose_name='Статус материала')

    creation_date = models.DateTimeField(
        **NULLABLE, verbose_name='Дата создания')
    last_update = models.DateTimeField(
        **NULLABLE, verbose_name='Дата последнего обновления')

    media = models.ManyToManyField(
        blank=True, to=Media, related_name='material_media')
    section = models.ForeignKey(
        **NULLABLE, to=Section, on_delete=models.SET_NULL,
        related_name='material_section')

    def __str__(self):
        return (f'Name: {self.name}, Status: {self.status}, '
                f'Created: {self.creation_date}')

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
        ordering = 'name',
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_last_update_after_creation_date',
                check=models.Q(last_update__gte=models.F('creation_date'))
            )
        ]

    def clean(self):
        # Проверка на соответствие статуса материала статусу раздела
        if self.section.status == 'ARCHIVED' and self.status != 'ARCHIVED':
            raise ValidationError('Материал должен иметь тот же статус,'
                                  'что и родительский раздел')
        elif self.section.status == 'CLOSED' and self.status != 'CLOSED':
            raise ValidationError('Материал должен иметь тот же статус,'
                                  'что и родительский раздел')

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None, *args, **kwargs):
        # Автозапись даты создания
        if not self.creation_date:
            self.creation_date = timezone.now()
        # Автозапись даты обновления
        if not self.last_update:
            self.last_update = timezone.now()
        super().save(force_insert, force_update, using, update_fields,
                     *args, **kwargs)


class TestAnswer(models.Model):
    """Модель ответа на вопрос теста"""
    answer = models.CharField(
        max_length=1_000, verbose_name='Выбор варианта ответа')

    def __str__(self):
        return f'Answer: {self.answer}'

    class Meta:
        verbose_name = 'ответ на тест'
        verbose_name_plural = 'ответы на тест'
        ordering = 'answer',


class TestQuestion(models.Model):
    """Модель вопроса теста"""
    question = models.TextField(
        verbose_name='Вопрос')
    answer = models.OneToOneField(
        to=TestAnswer, on_delete=models.CASCADE,
        related_name='testquestion_answer')
    choices = models.ManyToManyField(
        to=TestAnswer, related_name='testquestion_choices')
    media = models.ManyToManyField(
        blank=True, to=Media, related_name='testquestion_media')

    def __str__(self):
        return f'Question: {self.question}, {self.answer}'

    class Meta:
        verbose_name = 'вопрос на тест'
        verbose_name_plural = 'вопросы на тесты'
        ordering = 'question',


class Test(models.Model):
    """Модель теста"""
    material = models.OneToOneField(
        **NULLABLE, to=Material, on_delete=models.CASCADE,
        related_name='test_material')
    question = models.ManyToManyField(
        to=TestQuestion, related_name='test_question')

    creation_date = models.DateTimeField(
        **NULLABLE, verbose_name='Дата создания')
    last_update = models.DateTimeField(
        **NULLABLE, verbose_name='Дата последнего обновления')

    def __str__(self):
        question_list = ', '.join(
            [str(question.question) for question in self.question.all()])
        return f'Question: {question_list}, Created: {self.creation_date}'

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'
        ordering = 'material',
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_last_update_after_creation_date',
                check=models.Q(last_update__gte=models.F('creation_date')),
            )
        ]

    def clean(self):
        # Проверка даты обновления позже или одинаковой с датой создания
        if self.last_update < self.creation_date:
            raise models.ValidationError(
                'Дата обновления не может быть раньше даты создания'
            )

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None, *args, **kwargs):
        # Автозапись даты создания
        if not self.creation_date:
            self.creation_date = timezone.now()
        # Автозапись даты обновления
        if not self.last_update:
            self.last_update = timezone.now()
        super().save(force_insert, force_update, using, update_fields,
                     *args, **kwargs)
