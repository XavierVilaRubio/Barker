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
		fields = ['username', 'password']

		help_texts = {
			'password': 'La contraseña debe contener, como mínimo, 8 carácteres incluyendo un símbolo, una mayúscula, una minúscula y un número',
		}
		
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
			'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'password'})
		}

class BarkForm(forms.ModelForm):
	class Meta:
		model = Bark
		fields = [
			'text',
			'media',
		]