from django.contrib import admin
from django.utils.safestring import mark_safe

from women.models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    """Дополнительный фильтр статей в админ панели"""

    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """Названия фильтров"""

        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        """Действия при фильтрации"""

        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    """Таблица статей в админ-панели"""

    list_display = ('title', 'post_photo', 'time_create', 'is_published')
    list_display_links = ('title', )
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tags']
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    filter_horizontal = ['tags']
    readonly_fields = ['post_photo']

    @admin.display(description="Изображение")
    def post_photo(self, women: Women):
        """Отображение фото в таблице"""

        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        """Действие - публикация выделенных записей"""

        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        """Действие - отмена публикации выделенных записей"""

        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Таблица категорий в админ-панели"""

    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
