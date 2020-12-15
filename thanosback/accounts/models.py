



from django.db import models
#from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	def __str__(self):
		return self.name

class history(models.Model):
	username=models.CharField(max_length=500,default="",blank=True)
	id = models.AutoField(primary_key=True)
	search=models.CharField(max_length=500,default="P-0001",null=True)
	image=models.CharField(max_length=500,default="P-0001",null=True)
	created_at = models.DateField(auto_now_add=True)
	likes =models.ManyToManyField(User,related_name='like')

