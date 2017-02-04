from __future__ import unicode_literals
from datetime import datetime    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
	user = models.OneToOneField(User)
	bio = models.CharField(max_length=430,blank=True)
	age = models.IntegerField(default=0,blank=True)
	following = models.ManyToManyField('self',symmetrical=False)
	profile_picture = models.FileField(upload_to="socialnetwork/media/photos", blank=True)

	def __unicode__(self):
		return self.user.username

class Post(models.Model):
	user = models.ForeignKey(Profile)
	userId = models.IntegerField(default=0,blank=True)
	content = models.CharField(max_length=500) 
	date  = models.DateField()
	time = models.TimeField()
	public = models.BooleanField()
	username = models.CharField(max_length=20,blank=True)

	def __unicode__(self):
		return self.content

class Comment(models.Model):
	author 		= models.ForeignKey(Profile)
	post 		= models.ForeignKey(Post)
	body 		= models.CharField(max_length=256)
	datetime 	= models.DateTimeField()
