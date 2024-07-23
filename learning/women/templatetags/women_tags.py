from django import template
import women.views as views

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories():
    return views.cats_db


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    return {"cats": views.cats_db, "cat_selected": cat_selected}
