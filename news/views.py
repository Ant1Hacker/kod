from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse

from .models import News, Category


def news_list(request):
    news = News.objects.filter(published=True).select_related('category').order_by('-id')[1:]
    last_new = News.objects.filter(published=True).order_by('-id')[0]
    paginator = Paginator(news, 4)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        news = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'news/list_ajax.html',
                      {'section': 'home',
                       'news': news,
                       'title': 'Kod'})
    return render(request,
                  'news/news_list.html',
                  {'section': 'home',
                   'last_new': last_new,
                   'news': news,
                   'title': 'Kod'})


# class HomeNews(ListView):
#     model = News
#     template_name = 'news/news_list.html'
#     context_object_name = 'news'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Home news'
#         context['section'] = 'home'
#         context['last'] = 1
#         return context
#
#     def get_queryset(self):
#         return News.objects.filter(published=True).select_related('category')


def news_by_category(request, category_slug):
    news = News.objects.filter(category__slug=category_slug,
                               published=True).select_related('category').order_by('-id')[1:]
    last_new = News.objects.filter(category__slug=category_slug, published=True).order_by('-id')[0]
    paginator = Paginator(news, 3)
    page = request.GET.get('page')
    title = Category.objects.get(slug=category_slug)
    count = News.objects.filter(category__slug=category_slug, published=True).count()
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        news = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'news/list_ajax.html',
                      {'section': 'category',
                       'news': news, 'title': title,
                       'count': count})
    return render(request,
                  'news/news_category.html',
                  {'section': 'category',
                   'last_new': last_new,
                   'news': news, 'title': title,
                   'count': count})


# class NewsByCategory(ListView):
#     model = News
#     template_name = 'news/news_category.html'
#     context_object_name = 'news'
#     allow_empty = False
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = Category.objects.get(slug=self.kwargs['category_slug'])
#         context['count'] = News.objects.filter(category__slug=self.kwargs['category_slug'],
#                                                published=True).count()
#         context['section'] = 'category'
#         return context
#
#     def get_queryset(self, **kwargs):
#         return News.objects.filter(category__slug=self.kwargs['category_slug'],
#                                    published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'
    slug_url_kwarg = 'news_slug'
    extra_context = {
        'section': 'view_news',
    }
