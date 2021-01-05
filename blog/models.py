from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce import HTMLField

from workouts.models import Category


class Article(models.Model):

    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    content = HTMLField()
    image = models.ImageField(max_length=100, upload_to='article')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})
