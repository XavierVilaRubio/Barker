from django.urls import path
from . import views




urlpatterns = [
    path('',            views.loginOptions),    # Choose to login or register
    path('login/',      views.login),           # Login
    path('register/',   views.register),        # Register
    path('home/',       views.home),            # Home page (feed)
]
