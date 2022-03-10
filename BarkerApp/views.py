from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from .forms import UserForm, ProfileForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile, Request
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


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
            return redirect('home')

    context = {
        'form': form,
    }

    return render(request, 'registration/login.html', context)

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

@login_required(login_url='/accounts/login/')
def home_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'home.html', context)

def get_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    try:
        request.user.profile.connected_profiles.get(user=user)
        following = True
    except ObjectDoesNotExist:
        following = False
        
    context = {
        'user': user,
        'following': following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/signin/')
def requests_view(request):
    requests = Request.objects.filter(reciver=request.user.id)

    context = {
        'requests': requests
    }

    return render(request, 'requests.html', context)

def send_request(request, username):
    sender_user = request.user
    sender_profile = sender_user.profile
    reciver_user = User.objects.get(username=username)
    reciver_profile = reciver_user.profile
    req = Request(sender=sender_profile, reciver=reciver_profile)
    req.save()

    return redirect('/')

def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    request.user.profile.connected_profiles.remove(user.profile)
    user.profile.connected_profiles.remove(request.user.profile)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def accept_request(request, username):
    sender_user = User.objects.get(username=username)
    sender_profile = sender_user.profile
    reciver_user = request.user
    reciver_profile = reciver_user.profile
    
    req = get_object_or_404(Request, sender=sender_profile, reciver=reciver_profile)
    req.delete()
    
    sender_profile.connected_profiles.add(reciver_profile)
    reciver_profile.connected_profiles.add(sender_profile)

    return redirect('/')