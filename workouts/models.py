from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.fields import DateField

from django.utils.safestring import mark_safe
from tinymce import HTMLField


class Category(models.Model):
    TYPE = (
        ('Body Building', 'Body Building'),
        ('Aerobic', 'Aerobic'),
        ('Weight Lifting', 'Weight Lifting'),
        ('Yoga', 'Yoga'),
        ('Crossfit', 'Crossfit'),
        ('Body Fit', 'Body Fit'),
        ('Gym', 'Gym'),
    )
    name = models.CharField(max_length=100, choices=TYPE)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Exercise(models.Model):
    image = models.ImageField(upload_to='exercises')
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = HTMLField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('workouts:exercise_detail', kwargs={
            'exercise_id': self.id
        })


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='members')

    def __str__(self) -> str:
        return self.user.username


class Workout(models.Model):
    STATUS = (
        ('In progress', 'In progress'),
        ('Finished', 'Finished')
    )
    name = models.CharField(max_length=100)
    member = models.ForeignKey(
        Member, null=True, blank=True, on_delete=models.CASCADE)
    date_of_training = DateField()
    exercise = models.ManyToManyField(Exercise)
    status = models.CharField(
        max_length=100, null=True, blank=True, choices=STATUS)

    def __str__(self) -> str:
        return self.name


class Coach(models.Model):
    name = models.CharField(max_length=100)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='coach')
    category = models.ManyToManyField(Category)
    bio = HTMLField()

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" style="width: 250px;" />')

    def __str__(self):
        return self.name


class Slider(models.Model):
    image = models.ImageField(upload_to='banner')
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" style="width: 250px;" />')


class Banner(models.Model):
    PAGES = (
        ('about', 'about'),
        ('contact', 'contact'),
        ('blog', 'blog'),
        ('coach', 'coach'),
        ('program', 'program'),
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banner')
    created = models.DateTimeField(auto_now_add=True)
    page = models.CharField(max_length=100, choices=PAGES)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" style="width: 250px;" />')

    def __str__(self) -> str:
        return self.title
