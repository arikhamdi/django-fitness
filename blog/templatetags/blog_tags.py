from django import template

from blog.models import Post

register = template.Library()


@register.inclusion_tag('footer.html')
def show_latest_posts():
    latest_posts = Post.objects.all().order_by('-created')[:2]
    return {'latest_posts': latest_posts}
