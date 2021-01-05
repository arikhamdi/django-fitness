from django.shortcuts import render, get_object_or_404

from .models import Article
from workouts.models import Category, Banner


def counter_categories():
    categories = Category.objects.all().order_by('name')
    counter = {}
    for category in categories:
        counter[category] = Article.objects.filter(
            category=category).count()
    print(counter)
    return counter


def home(request):
    articles = Article.objects.all().order_by('-created')
    banner = Banner.objects.filter(page='blog').first
    context = {
        'articles': articles,
        'counter': counter_categories(),
        'banner': banner,
    }
    return render(request, 'blog/index.html', context)


def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {
        'article': article,
        'counter': counter_categories()
    }
    return render(request, 'blog/blog_detail.html', context)
