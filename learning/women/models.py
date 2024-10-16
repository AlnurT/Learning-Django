from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    """Менеджер фильтрации опубликованных статей"""

    def get_queryset(self):
        """Список опубликованных статей"""
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    """Таблица основных данных статей"""

    class Status(models.IntegerChoices):
        """Статус статьи"""

        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True,
                            validators=[
                                MinLengthValidator(5),
                                MaxLengthValidator(100),
                            ])
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name="Время изменения")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фото")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Статус"
    )
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,
                            related_name='posts', verbose_name="Категории")
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True, related_name='woman',
                                   verbose_name="Муж")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags',
                                  verbose_name="Тэги")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='posts', null=True,
                               default=None, blank=True)

    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        """Дополнительные параметры модели"""

        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        """Строковое представление"""

        return self.title

    def get_absolute_url(self):
        """URL модели"""

        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    """Таблица профессий для женщин"""

    name = models.CharField(max_length=100, db_index=True,
                            verbose_name="Категория")
    slug = models.CharField(max_length=255, unique=True, db_index=True)

    class Meta:
        """Дополнительные параметры модели"""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Строковое представление"""
        return self.name

    def get_absolute_url(self):
        """URL модели"""
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    """Таблица тегов для женщин"""

    tag = models.CharField(max_length=100, db_index=True)
    slug = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        """Строковое представление"""
        return self.tag

    def get_absolute_url(self):
        """URL модели"""
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    """Таблица данных мужей известных женщин"""

    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(default=0, blank=True)

    def __str__(self):
        """Строковое представление"""
        return self.name
