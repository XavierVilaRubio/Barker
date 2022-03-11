from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from BarkerApp.models import Profile, Bark

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = [
			'username',
			'password1',
			'password2',
			'email',
		]

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [
			'bio',
			'avatar',
		]

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username',
			'password'
		]

class BarkForm(forms.ModelForm):
	class Meta:
		model = Bark
		fields = [
			'text',
			'media',
		]