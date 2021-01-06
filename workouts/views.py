from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.db.models import Count

from .models import Exercise, Member, Workout, Banner, Coach, Category
from blog.models import Post
from .forms import WorkoutForm, MemberForm, Comments_coachForm


def index(request):
    recent_posts = Post.objects.all().order_by('-created')[:3]

    # Display categories on homepage sorted by number of exercices desc
    most_categories = Category.objects.annotate(
        number_of_exercises=Count('exercise'))
    categories = {}
    for cat in most_categories:
        # get the category only if it has exercises in it
        if cat.number_of_exercises > 0:
            categories[cat.title] = [cat.number_of_exercises,
                                     cat.slug, cat.image, cat.description]
    # dict sorted by number of exercises
    sorted_categories = sorted(
        categories.items(), key=lambda x: x[1][0], reverse=True)

    context = {
        'recent_posts': recent_posts,
        'categories': sorted_categories[:4]
    }
    return render(request, 'index.html', context)


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    context = {
        'exercise': exercise
    }
    return render(request, 'exercise_detail.html', context)


def member_page(request):
    member = Member.objects.get(user=request.user)
    workouts = member.workout_set.all()
    total_workouts = workouts.count()
    in_progres = member.workout_set.filter(status='In progress').count()
    finished = member.workout_set.filter(status='Finished').count()
    form = MemberForm()
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()

    context = {
        'member': member,
        'workouts': workouts,
        'total_workouts': total_workouts,
        'in_progres': in_progres,
        'finished': finished,
        'form': form,
    }
    return render(request, 'user/member.html', context)


def create_workout(request):
    member = Member.objects.get(user=request.user)
    form = WorkoutForm(request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.user, request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('workouts:member_page')
    context = {
        'form': form
    }
    return render(request, 'workout_form.html', context)


def update_workout(request, id):
    workout = Workout.objects.get(id=id)
    form = WorkoutForm(request.user, instance=workout)

    if request.method == 'POST':
        form = WorkoutForm(request.user, request.POST, instance=workout)

        if form.is_valid():
            form.instance.workout = workout
            form.save()
            return redirect('workouts:member_page')
    context = {
        'form': form
    }
    return render(request, 'workout_form.html', context)


def program(request):
    categories = Category.objects.all().order_by('title')
    context = {
        'categories': categories,
        'banner': Banner.objects.filter(page='program').first
    }
    return render(request, 'program.html', context)


def program_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    exercises = Exercise.objects.filter(category=category)
    context = {
        'category': category,
        'exercises': exercises
    }
    return render(request, 'program_detail.html', context)


def coach(request):
    coaches = Coach.objects.all().order_by('name')
    context = {
        'coaches': coaches,
        'banner': Banner.objects.filter(page='coach').first,
    }
    return render(request, 'coach.html', context)


def coach_detail(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)
    form = Comments_coachForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.coach = coach
            form.save()
            return redirect(reverse('workouts:coach_detail', kwargs={
                'coach_id': coach.id
            }))
    context = {
        'coach': coach,
        'form': form,
        'counter_comments': coach.comments_coach.count()
    }
    return render(request, 'coach_detail.html', context)


def about(request):
    return render(request, 'about.html', {'banner': Banner.objects.filter(page='about').first})


def contact(request):
    return render(request, 'contact.html', {'banner': Banner.objects.filter(page='contact').first})


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
