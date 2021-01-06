from django.urls import path

from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.index, name='home'),
    path('exercise/<int:exercise_id>',
         views.exercise_detail, name='exercise_detail'),

    path('program', views.program, name='program'),
    path('program/<slug:slug>', views.program_detail, name='program_detail'),
    path('coach', views.coach, name='coach'),
    path('coach/<int:coach_id>', views.coach_detail, name='coach_detail'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    # Members
    path('register', views.register_page, name='register_page'),
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_page, name='logout_page'),
    path('member', views.member_page, name='member_page'),
    path('create_workout', views.create_workout, name='create_workout'),
    path('update_workout/<int:id>', views.update_workout, name='update_workout'),
]
