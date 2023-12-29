from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField

from education.apps import EducationConfig

app_name = EducationConfig.name

NULLABLE = {'blank': True, 'null': True}


class Media(models.Model):
    """Модель медиа"""
    name = models.CharField(
        max_length=100, verbose_name='Название',
        help_text='Не более 100 символов')

    creation_date = models.DateTimeField(
        **NULLABLE, verbose_name='Дата создания')

    local_image = models.ImageField(
        **NULLABLE, upload_to='education/media/images/%Y/%m%d/',
        verbose_name='Локальное изображение',
        help_text='Только одно поле может быть выбрано')
    external_image = models.URLField(
        **NULLABLE, verbose_name='Внешнее изображение',
        help_text='Только одно поле может быть выбрано')
    local_video = models.FileField(
        **NULLABLE, upload_to='education/media/videos/%Y/%m%d/',
        verbose_name='Локальное видео',
        help_text='Только одно поле может быть выбрано')
    external_video = models.URLField(
        **NULLABLE, verbose_name='Внешнее видео',
        help_text='Только одно поле может быть выбрано')
    local_audio = models.FileField(
        **NULLABLE, upload_to='education/media/audios/%Y/%m%d/',
        verbose_name='Локальное аудио',
        help_text='Только одно поле может быть выбрано')
    external_audio = models.URLField(
        **NULLABLE, verbose_name='Внешнее аудио',
        help_text='Только одно поле может быть выбрано')

    def __str__(self):
        media_links = [self.name]
        if self.local_image:
            media_links.append(str(self.local_image))
        if self.external_image:
            media_links.append(self.external_image)
        if self.local_video:
            media_links.append(str(self.local_video))
        if self.external_video:
            media_links.append(self.external_video)
        if self.local_audio:
            media_links.append(str(self.local_audio))
        if self.external_audio:
            media_links.append(self.external_audio)

        return (f'Название: {self.name}, '
                f'Дата создания: {self.creation_date}, '
                f'Медиа: {", ".join(media_links)}')

    class Meta:
        verbose_name = 'медиа'
        verbose_name_plural = 'медиа'
        ordering = 'name',

    def clean(self):
        # Проверка на обязательный выбор только одного медиа файла
        sum_of_fields = sum(bool(field) for field in [
            self.local_image, self.external_image,
            self.local_video, self.external_video,
            self.local_audio, self.external_audio
        ])
        if sum_of_fields == 0:
            raise ValidationError('Медиа файл должен быть указан')
        if sum_of_fields > 1:
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
        max_length=100, verbose_name='Название',
        help_text='Не более 100 символов')
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
        **NULLABLE, verbose_name='Дата последнего обновления',
        help_text='Дата обновления должна быть больше даты создания')

    base_price = MoneyField(
        max_digits=14, decimal_places=2, default=0, default_currency='RUB',
        verbose_name='Базовая цена')

    media = models.ManyToManyField(
        blank=True, to=Media, related_name='section_media',
        verbose_name='Медиа')

    def __str__(self):
        return (f'Имя: {self.name}, Статус: {self.status}, '
                f'Дата создания: {self.creation_date}, '
                f'Базовая цена: {self.base_price}')

    class Meta:
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'
        ordering = 'name',
        constraints = [
            # Проверка даты обновления позже или одинаковой с датой создания
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_last_update_after_creation_date',
                check=models.Q(last_update__gte=models.F('creation_date')),
            )
        ]

    def clean(self):
        # Проверка даты обновления позже или одинаковой с датой создания
        if self.last_update < self.creation_date:
            raise ValidationError(
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
        max_length=100, verbose_name='Название',
        help_text='Не более 100 символов')
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
        **NULLABLE, verbose_name='Дата последнего обновления',
        help_text='Дата обновления должна быть больше даты создания')

    media = models.ManyToManyField(
        blank=True, to=Media, related_name='material_media',
        verbose_name='Медиа')
    section = models.ForeignKey(
        **NULLABLE, to=Section, on_delete=models.SET_NULL,
        related_name='material_section', verbose_name='Раздел')

    def __str__(self):
        return (f'Имя: {self.name}, Статус: {self.status}, '
                f'Дата создания: {self.creation_date}')

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
        ordering = 'name',
        constraints = [
            # Проверка даты обновления позже или одинаковой с датой создания
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_last_update_after_creation_date',
                check=models.Q(last_update__gte=models.F('creation_date'))
            )
        ]

    def clean(self):
        # Проверка даты обновления позже или одинаковой с датой создания
        if self.last_update < self.creation_date:
            raise ValidationError(
                'Дата обновления не может быть раньше даты создания'
            )
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
        max_length=1_000, verbose_name='Выбор варианта ответа',
        help_text='Не более 1000 символов')

    def __str__(self):
        return f'Ответ: {self.answer}'

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
        related_name='testquestion_answer', verbose_name='Ответ')
    choices = models.ManyToManyField(
        to=TestAnswer, related_name='testquestion_choices',
        verbose_name='Варианты ответа')
    media = models.ManyToManyField(
        blank=True, to=Media, related_name='testquestion_media',
        verbose_name='Медиа')

    def __str__(self):
        return f'Вопрос: {self.question}, Ответ:{self.answer}'

    class Meta:
        verbose_name = 'вопрос на тест'
        verbose_name_plural = 'вопросы на тесты'
        ordering = 'question',


class Test(models.Model):
    """Модель теста"""
    material = models.OneToOneField(
        **NULLABLE, to=Material, on_delete=models.CASCADE,
        related_name='test_material', verbose_name='Материал')
    question = models.ManyToManyField(
        to=TestQuestion, related_name='test_question',
        verbose_name='Вопрос')

    creation_date = models.DateTimeField(
        **NULLABLE, verbose_name='Дата создания')
    last_update = models.DateTimeField(
        **NULLABLE, verbose_name='Дата последнего обновления',
        help_text='Дата обновления должна быть больше даты создания')

    def __str__(self):
        question_list = ', '.join(
            [str(question.question) for question in self.question.all()])
        return f'Вопрос: {question_list}, Дата создания: {self.creation_date}'

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'
        ordering = 'material',
        constraints = [
            # Проверка даты обновления позже или одинаковой с датой создания
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_last_update_after_creation_date',
                check=models.Q(last_update__gte=models.F('creation_date')),
            )
        ]

    def clean(self):
        # Проверка даты обновления позже или одинаковой с датой создания
        if self.last_update < self.creation_date:
            raise ValidationError(
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
