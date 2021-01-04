from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Exercise, Member


def index(request):
    return render(request, 'index.html', {})


def bodybuilding(request):
    bodyBuildingExercises = Exercise.objects.filter(
        category__category='Body Building')
    context = {
        'bodyBuildingExercises': bodyBuildingExercises
    }
    return render(request, 'bodybuilding.html', context)


def aerobic(request):
    aerobic = Exercise.objects.filter(category__category='Aerobic')
    context = {
        'aerobic': aerobic
    }
    return render(request, 'aerobic.html', context)


def weightlifting(request):
    weightlifting = Exercise.objects.filter(
        category__category='Weight Lifting')
    context = {
        'weightlifting': weightlifting
    }
    return render(request, 'weightlifting.html', context)


def yoga(request):
    yoga = Exercise.objects.filter(category__category='Yoga')
    context = {
        'yoga': yoga
    }
    return render(request, 'yoga.html', context)


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    context = {
        'exercise': exercise
    }
    return render(request, 'exercise_detail.html', context)


def member_page(request):
    member = Member.objects.get(user=request.user)
    context = {
        'member': member
    }
    return render(request, 'user/member.html', context)


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Member.objects.create(user=user)
            return redirect('workouts:login_page')

    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('workouts:home')

    return render(request, 'user/login.html')


def logout_page(request):
    logout(request)
    return redirect('workouts:login_page')
