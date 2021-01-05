from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Post, Comment
from .forms import CommentForm
from workouts.models import Category, Banner, Member


def counter_categories():
    categories = Category.objects.all().order_by('name')
    counter = {}
    for category in categories:
        counter[category] = Post.objects.filter(
            category=category).count()
    print(counter)
    return counter


def home(request):
    posts = Post.objects.all().order_by('-created')
    banner = Banner.objects.filter(page='blog').first
    context = {
        'posts': posts,
        'counter': counter_categories(),
        'banner': banner,
    }
    return render(request, 'blog/index.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        member = get_object_or_404(Member, user=request.user)
        if form.is_valid():
            form.instance.member = member
            form.instance.post = post
            form.save()
            return redirect(reverse('blog:blog_detail', kwargs={
                'slug': post.slug
            }))
    context = {
        'post': post,
        'counter': counter_categories(),
        'form': form,
        'counter_comments': post.comments.count()
    }
    return render(request, 'blog/blog_detail.html', context)


def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    post = comment.post
    comment.delete()
    return redirect(reverse('blog:blog_detail', kwargs={
        'slug': post.slug
    }))

