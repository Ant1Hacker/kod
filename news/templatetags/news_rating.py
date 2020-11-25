from django import template
from django.db.models import Count, F

from news.models import Category, News, Tag

register = template.Library()


@register.inclusion_tag('news/rating_news.html')
def news_rate():
    # rating_news = News.objects.filter(views__gt=0).order_by('-views')
    rating_news = News.objects.all().order_by('-views')[:5]
    return {'rating_news': rating_news}
