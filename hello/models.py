from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Usermodel(models.Model):
	user = models.OneToOneField(User)
	customerID=models.IntegerField(null=True,blank=True)	
	def __str__(self):
		return u'%s  %s  %d'%(self.user.username,self.user.first_name,self.customerID)



