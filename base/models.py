from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Events(models.Model):
    event_name = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    createdTime=models.DateTimeField(auto_now_add=True)
    fields =['events_name','price','quantity']
 
    def __str__(self):
           return self.event_name


class PrivetInformation(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    age = models.FloatField()
    email = models.EmailField(default='example@domain.com')
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=75)
    postalcode = models.FloatField()
    avatar = models.ImageField(null=True,blank=True,default='/default.photopng.png')
    def __str__(self):
        return self.firstname