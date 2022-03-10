from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, ProfileForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.

def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')

    context = {
        'form': form,
    }

    return render(request, 'signin.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)

    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

        login(request, user)

        return redirect('/')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'registration/register.html', context)

@login_required(login_url='/signin/')
def home_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'home.html', context)

def get_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/signin/')
def edit_profile_view(request):

    user_form = UserForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, instance=request.user.profile)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()

        return redirect('/')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'edit_profile.html', context)