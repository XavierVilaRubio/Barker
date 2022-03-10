from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	bio = models.CharField(max_length=160)
	avatar = models.ImageField(null=True, blank=True)

	def __str__(self) -> str:
		return self.user.username

	def get_absolute_url(self):
		return reverse('profile', kwargs={'user':self})
		
