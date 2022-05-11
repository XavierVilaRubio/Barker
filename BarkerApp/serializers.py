from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Request, Bark

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'username',
			'email'
		]

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = [
			'user',
			'bio',
			'avatar',
			'barks',
			'connected_profiles',
		]

class RequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Request
		fields = [
			'date',
			'sender',
			'reciver'
		]

class BarkSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bark
		fields = [
			# 'reply_to',
			'text',
			'media',
			'date',
			'replies'
		]
