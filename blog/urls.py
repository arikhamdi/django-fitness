from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>', views.blog_detail, name='blog_detail'),
    path('delete/<int:id>', views.comment_delete, name='comment_delete'),
]
