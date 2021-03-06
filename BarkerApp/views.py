from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.forms import UserChangeForm

from .forms import UserForm, ProfileForm, LoginForm, BarkForm
from .models import Profile, Request, Bark
from .utils import parseLinks

# Create your views here.

def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)

    if form.is_valid():
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
    profile_form = ProfileForm(request.POST or None, request.FILES or None)

    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

        login(request, user)

        return redirect('home')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'registration/register.html', context)

@login_required(login_url='/accounts/login/')
def home_view(request):
    connections = request.user.profile.connected_profiles.all()
    barks = []
    for profile in connections:
        barks += Bark.objects.filter(author=profile)
    barks += Bark.objects.filter(author=request.user.profile)
    barks.sort(key=lambda x: x.date, reverse=True)
    context = {
        'user': request.user,
        'connections': connections,
        'barks': barks
    }
    return render(request, 'home.html', context)

def get_profile_view(request, username):
    user = get_object_or_404(User, username=username)

    barks = Bark.objects.filter(author=user.profile)

    status = 'follow'
    if request.user.username != username and request.user.is_authenticated:
        print('si')
        if request.user.profile.connected_profiles.filter(user=user).exists():
            status = 'unfollow'
        elif Request.objects.filter(sender=user.profile, reciver=request.user.profile).exists():
            status = 'accept'
        elif Request.objects.filter(sender=request.user.profile, reciver=user.profile).exists():
            status = 'cancel'
        
    context = {
        'user': user,
        'status': status,
        'barks': barks
    }
    return render(request, 'profile/profile.html', context)

@login_required(login_url='/accounts/login/')
def edit_profile_view(request):
    user_form = UserForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()

        return redirect('/')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile/edit_profile.html', context)

@login_required(login_url='/accounts/login/')
def requests_view(request):
    requests = Request.objects.filter(reciver=request.user.id)

    context = {
        'requests': requests
    }

    return render(request, 'requests.html', context)

@login_required(login_url='/accounts/login/')
def send_request(request, username):
    sender_user = request.user
    sender_profile = sender_user.profile
    reciver_user = User.objects.get(username=username)
    reciver_profile = reciver_user.profile

    if not Request.objects.filter(sender=sender_profile, reciver=reciver_profile).exists():
        req = Request(sender=sender_profile, reciver=reciver_profile)
        req.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/accounts/login/')
def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    request.user.profile.connected_profiles.remove(user.profile)
    user.profile.connected_profiles.remove(request.user.profile)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/accounts/login/')
def accept_request(request, username):
    sender_user = User.objects.get(username=username)
    sender_profile = sender_user.profile
    reciver_user = request.user
    reciver_profile = reciver_user.profile
    
    req = get_object_or_404(Request, sender=sender_profile, reciver=reciver_profile)
    req.delete()
    
    sender_profile.connected_profiles.add(reciver_profile)
    reciver_profile.connected_profiles.add(sender_profile)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/accounts/login/')
def cancel_request(request, username):
    sender_user = request.user
    sender_profile = sender_user.profile
    reciver_user = User.objects.get(username=username)
    reciver_profile = reciver_user.profile

    req = Request.objects.filter(sender=sender_profile, reciver=reciver_profile)
    req.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/accounts/login/')
def post_bark(request):
   
    form = BarkForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        bark = form.save(commit=False)
        bark.text = parseLinks(bark.text)
        bark.author = request.user.profile
        bark.save()

        return redirect(bark.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'bark/post_bark.html', context)

def get_bark(request, bark_id):
   
    bark = get_object_or_404(Bark, id=bark_id)

    context = {
        'bark': bark,
    }

    return render(request, 'bark/bark.html', context)

@login_required(login_url='/accounts/login/')
def delete_bark(request, bark_id):
    bark = get_object_or_404(Bark, id=bark_id)
    bark.delete()
    
    return redirect(request.user.profile.get_absolute_url())

@login_required(login_url='/accounts/login/')
def edit_bark(request, bark_id):
    bark = get_object_or_404(Bark, id=bark_id)
    form = BarkForm(request.POST or None, request.FILES or None, instance=bark)

    if form.is_valid():
        bark = form.save()

        return redirect(bark.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'bark/edit_bark.html', context)

@login_required(login_url='/accounts/login/')
def reply_bark(request, bark_id):
   
    original_bark = get_object_or_404(Bark, id=bark_id)
    form = BarkForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        bark = form.save(commit=False)
        bark.author = request.user.profile
        bark.reply_to = original_bark
        bark.save()

        original_bark.replies.add(bark)
        original_bark.save()

        return redirect(bark.get_absolute_url())

    context = {
        'form': form,
        'bark': original_bark
    }

    return render(request, 'bark/reply_bark.html', context)

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import generics, viewsets, permissions, status
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, RequestSerializer, BarkSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ProfileViewSet(viewsets.ModelViewSet):
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk):
        try:
            user = User.objects.get(username=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            profile = Profile.objects.get(user=user)
            barks = Bark.objects.filter(author=profile)
            serialized_user = UserSerializer(user)
            serialized_profile = ProfileSerializer(profile)
            serialized_barks = BarkSerializer(barks, many=True)
            data = {
                'user': serialized_user.data,
                'profile': serialized_profile.data,
                'barks': serialized_barks.data
            }
            return Response(data=data, status=status.HTTP_200_OK)


class RequestViewSet(viewsets.ModelViewSet):
    
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.AllowAny]

class BarkViewSet(viewsets.ModelViewSet):
    
    queryset = Bark.objects.all()
    serializer_class = BarkSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def getFriends(request):

    connections = request.user.profile.connected_profiles.all()
    users = []
    for profile in connections:
        users.append(profile.user)
    users_serialized = UserSerializer(users, many=True)
    return Response(data=users_serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getFriendsTimeline(request):

    connections = request.user.profile.connected_profiles.all()
    barks = []
    for profile in connections:
        barks += Bark.objects.filter(author=profile)
    barks += Bark.objects.filter(author=request.user.profile)
    barks.sort(key=lambda x: x.date, reverse=True)
    print(barks)

    serialized_barks = BarkSerializer(barks, many=True)
    return Response(data=serialized_barks.data, status=status.HTTP_200_OK)

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         return request.user and is_authenticated(request.user)
    #     else:
    #         return True

def barkView(request, bark_id):
    return render(request, 'bark/bark_new.html')

def profileView(request, username):
    return render(request, 'profile/profile_new.html')

def homeView(request):
    return render(request, 'home_new.html')
