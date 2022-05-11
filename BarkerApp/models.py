from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime    


# Create your models here.
class Bark(models.Model):
	reply_to = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name='parent_bark')
	text = models.TextField(max_length=280)
	media = models.ImageField(upload_to="barks_media/", null=True, blank=True)
	date = models.DateTimeField(default=datetime.now)
	replies = models.ManyToManyField("self", blank=True, symmetrical=False)
	
	def get_absolute_url(self):
		return reverse('bark', kwargs={'bark_id':self.id})

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	bio = models.CharField(max_length=160)
	avatar = models.ImageField(upload_to="profiles_avatar/",blank=True, null=True)
	connected_profiles = models.ManyToManyField("self", blank=True)
	barks = models.ManyToManyField(Bark, blank=True)

	def __str__(self) -> str:
		return self.user.username

	def get_absolute_url(self):
		return reverse('profile', kwargs={'username':self})
		
class Request(models.Model):
	date = models.DateTimeField(default=datetime.now)
	sender = models.ForeignKey(Profile, related_name='sended_by', on_delete=models.CASCADE)
	reciver = models.ForeignKey(Profile, related_name='recived_by',on_delete=models.CASCADE)

	def __str__(self) -> str:
		return "Request from {sender} to {reciver}".format(sender=self.sender, reciver=self.reciver)
