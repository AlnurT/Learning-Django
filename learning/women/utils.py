menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
]


class DataMixin:
    """Общие настройки для классов представлений"""

    paginate_by = 3
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title_page'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        """Общая настройка полей в таблице"""

        if self.title_page:
            context['title_page'] = self.title_page

        context['cat_selected'] = None
        context.update(kwargs)
        return context
