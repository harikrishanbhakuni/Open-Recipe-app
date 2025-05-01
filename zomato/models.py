from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 

class Order(models.Model):
    user = models.ForeignKey(User,on_delete= models.SET_NULL,null = True , blank= True)
    order_name = models.CharField(max_length=100)
    order_description = models.CharField(max_length=200)
    order_image = models.ImageField(upload_to= "orderimg")
    