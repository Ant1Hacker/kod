from django import template
from django.db.models import Count, F

from news.models import Category, News, Tag

register = template.Library()


@register.inclusion_tag('news/templatetags/sidebar.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('get_news',
                                                     filter=F('get_news__published'))).filter(cnt__gt=0)
    return {'categories': categories}
