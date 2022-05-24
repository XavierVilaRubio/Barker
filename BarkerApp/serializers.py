from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Request, Bark

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'username',
			'email',
			'first_name',
			'last_name'
		]

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = [
			'user',
			'bio',
			'avatar',
			'connected_profiles',
		]

class RequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Request
		fields = [
			'id',
			'date',
			'sender',
			'reciver'
		]

class BarkSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bark
		fields = [
			'id',
			'reply_to',
			'author',
			'text',
			'media',
			'date',
			'replies'
		]
