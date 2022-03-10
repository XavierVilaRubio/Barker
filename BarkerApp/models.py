from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    


# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	bio = models.CharField(max_length=160)
	avatar = models.ImageField(blank=True)
	connected_profiles = models.ManyToManyField("self", blank=True)

	def __str__(self) -> str:
		return self.user.username

	def get_absolute_url(self):
		return reverse('profile', kwargs={'user':self})
		
class Request(models.Model):
	date = models.DateTimeField(default=datetime.now)
	sender = models.ForeignKey(Profile, related_name='sended_by', on_delete=models.CASCADE)
	reciver = models.ForeignKey(Profile, related_name='recived_by',on_delete=models.CASCADE)

	def __str__(self) -> str:
		return "Request from {sender} to {reciver}".format(sender=self.sender, reciver=self.reciver)

class Bark(models.Model):
	reply_to = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
	author = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
	text = models.TextField(max_length=280)
	media = models.ImageField(null=True, blank=True)
	date = models.DateTimeField(default=datetime.now)
	replies = models.ManyToManyField("self", blank=True)
	
	def get_absolute_url(self):
		return reverse('bark', kwargs={'id':self.id})