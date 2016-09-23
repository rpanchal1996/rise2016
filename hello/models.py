from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Greeting(models.Model):
	when = models.DateTimeField('date created', auto_now_add=True)

class Coder(models.Model):
	user = models.OneToOneField(User)
	semester=models.IntegerField(null=True,blank=True)	
	def __str__(self):
		return u'%s  %s  %d'%(self.user.username,self.user.first_name,self.semester)

class Helper(models.Model):
	user = models.OneToOneField(User)
	experience=models.IntegerField(null=True,blank=True)	
	
	def __str__(self):
		return u'%s  %s  %d'%(self.user.username,self.user.first_name,self.semester)
