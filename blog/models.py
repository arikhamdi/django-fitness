from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce import HTMLField

from django.contrib.auth.models import User
from workouts.models import Category, Coach, Member


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    autor = models.ForeignKey(Coach, on_delete=models.CASCADE)
    content = HTMLField()
    image = models.ImageField(max_length=100, upload_to='article')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-created')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} on {self.post.title}"
