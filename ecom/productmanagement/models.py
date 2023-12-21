from django.db import models
from categorymanagement . models import Brand
# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [ ('men' ,'Men'),
                ('women', 'Women'),
                ('all', 'ALL')] 
    
    name = models.CharField(max_length = 100)
    category = models.CharField(max_length = 10,choices = CATEGORY_CHOICES, default = 'all')
    brand = models.ForeignKey(Brand,on_delete = models.CASCADE)
    original_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    selling_price = models.DecimalField(max_digits = 10,decimal_places = 2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    image1 = models.ImageField(upload_to='media/images/',blank=True)
    is_listed = models.BooleanField(default = True)
    
    def __str__(self) -> str:
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name = 'images', on_delete = models.CASCADE)
    images =  models.ImageField(upload_to='media/images/')
    image_number = models.PositiveIntegerField(blank = True)