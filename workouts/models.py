from django.db import models
from django.urls import reverse
from django.utils.text import slugify
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
    title = models.CharField(max_length=100, choices=TYPE)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='program')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('workouts:program_detail', kwargs={
            'slug': self.slug
        })


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
    image = models.ImageField(blank=True, null=True, upload_to='coach')
    category = models.ManyToManyField(Category)
    bio = HTMLField()

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" style="width: 250px;" />')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('workouts:coach_detail', kwargs={
            'coach_id': self.id
        })

    @property
    def get_comments(self):
        return self.comments_coach.all().order_by('-created')


class Comments_coach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    coach = models.ForeignKey(
        Coach, related_name='comments_coach', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} on {self.coach.name}"


class Insta_Gallery(models.Model):
    image = models.ImageField(upload_to='insta_gallery')
    created = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" style="width: 250px;" />')


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
