from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def indexView(request):
    if request.user.is_authenticated:
        return redirect('home')

    return redirect('login')

def loginView(request):
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

def registerView(request):
    
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
def homeView(request):
    context = {
        'user': request.user
    }
    return render(request, 'home.html', context)