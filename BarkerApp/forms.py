from django import forms
from django.contrib.auth.models import User
from BarkerApp.models import Profile, Bark

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username',
			'password',
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