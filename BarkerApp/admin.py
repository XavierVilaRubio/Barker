from django.contrib import admin
from BarkerApp.models import Profile, Request, Bark

# Register your models here.
admin.site.register(Profile)
admin.site.register(Request)
admin.site.register(Bark)