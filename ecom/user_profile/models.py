from django.db import models
from home.models import Customuser
from productmanagement.models import Product
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
    is_available = models.BooleanField(default = True,null = True, blank = True)
    
    def __str__(self) -> str:
        return f"{self.name}'s Address "
    
    
class Wallet(models.Model):
    user_id = models.ForeignKey(Customuser, on_delete = models.CASCADE)
    amount = models.IntegerField(null = True, blank = True) 
    
    def __str__(self):
        return self.user_id.first_name 
    
    
class ProductReview(models.Model):
    user = models.ForeignKey(Customuser, on_delete = models.SET_NULL,null = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE,null = True)
    rating = models.IntegerField(null = True, blank = True)
    review = models.TextField(null = True , blank = True)
    created_at = models.DateTimeField(auto_now = True,null = True,blank = True)
    
    def __str__(self):
        return f"{self.user} - {self.product}" 