# Generated by Django 3.1.4 on 2021-01-06 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0011_comments_coach'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coach',
            old_name='profile_pic',
            new_name='image',
        ),
    ]
