from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def loginOptions(request):
    return render(request, "BarkerApp/index.html")
def register(request):
    return render(request, "BarkerApp/register.html")

def login(request):
    return render(request, "BarkerApp/login.html")

def home(request):
    return render(request, "BarkerApp/home.html")