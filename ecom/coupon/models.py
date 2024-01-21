from django.db import models
from productmanagement.models import Product,Brand
# Create your models here.

class Coupen(models.Model):
    title = models.CharField(max_length = 100,blank = True,null = True)
    code = models.CharField(max_length = 20, unique = True)
    valid_from = models.DateField(null = True,blank = True)
    valid_to = models.DateField(null = True,blank = True)
    discount_amount = models.DecimalField(max_digits = 10, decimal_places = 2,null = True,default = 0)
    is_active = models.BooleanField(default = True , null = True)
    created_at = models.DateField(auto_now_add = True)
     
    def __str__(self):
        return self.title 
    
class BrandOffer(models.Model): 
    brand = models.ForeignKey(Brand , on_delete = models.CASCADE,null = True)
    offer_percentage = models.FloatField(null = True,blank = True,default = 0)
    is_active = models.BooleanField(default = True)
    created_at = models.DateField(auto_now_add = True)


class ProductOffer(models.Model):
    product = models.ForeignKey(Product , on_delete = models.CASCADE,null = True)
    offer_percentage = models.FloatField(null = True,blank = True,default = 0)
    is_active = models.BooleanField(default = True)
    created_at = models.DateField(auto_now_add = True)