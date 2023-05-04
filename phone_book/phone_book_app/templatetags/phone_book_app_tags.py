from django import template
from phone_book_app.models import *


register = template.Library()


@register.simple_tag(name='get_cats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.all(pk=filter)


@register.inclusion_tag('all_phone_cards.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}