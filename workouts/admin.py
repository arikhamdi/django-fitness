from django.contrib import admin
from .models import Category, Exercise, Member, Banner, Workout


class BannerAdmin(admin.ModelAdmin):
    list_display = ('image_tag',)


admin.site.register(Category)
admin.site.register(Exercise)
admin.site.register(Member)
admin.site.register(Workout)
admin.site.register(Banner, BannerAdmin)
