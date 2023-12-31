from django.db import models
from home.models import Customuser
# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(Customuser, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    district = models.CharField(max_length = 100)
    town = models.CharField(max_length = 100)
    house = models.CharField(max_length = 100)
    land_mark = models.CharField(max_length = 100,blank = True, null = True)
    pincode = models.IntegerField()
    number = models.CharField(max_length = 15)
    alternate_number = models.CharField(max_length = 15,blank = True, null = True)
    
    def __str__(self) -> str:
        return f"{self.name}'s Address "