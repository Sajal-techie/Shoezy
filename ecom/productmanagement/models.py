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
    
    def __str__(self) -> str:
        return self.name
    