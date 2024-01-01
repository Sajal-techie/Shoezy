from django.db import models
from productmanagement.models import Product
from home.models import Customuser
# Create your models here.


class Cart(models.Model):
    user_id = models.ForeignKey(Customuser, on_delete = models.CASCADE, null = True)
    product_id = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    quantity = models.PositiveIntegerField(default = 0)
    sub_total =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    
    
    def save(self, *args, **kwargs):
        self.sub_total = self.quantity * self.product_id.selling_price
        super().save(*args, **kwargs)
    
    
class Wishlist(models.Model):
    user_id = models.ForeignKey(Customuser, on_delete = models.CASCADE, null = True)
    product_id = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    added_at = models.DateField(auto_now_add = True)
    stock = models.CharField(max_length = 20, null = True,blank = True)
    