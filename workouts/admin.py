from django.contrib import admin
from .models import Category, Exercise, Member, Banner, Workout, Slider, Coach


class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image_tag',)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('page', 'image_tag',)


class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag',)


admin.site.register(Category)
admin.site.register(Exercise)
admin.site.register(Member)
admin.site.register(Workout)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Banner, BannerAdmin)
