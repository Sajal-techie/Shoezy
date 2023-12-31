from django.db import models
from home.models import Customuser
from user_profile.models import Address
from productmanagement.models import Product
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(Customuser, on_delete= models.SET_NULL, null = True,blank = True) 
    address = models.ForeignKey(Address, on_delete= models.SET_NULL,null = True,blank = True) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank = True,null = True)
    order_date = models.DateField(auto_now_add = True)
    payment_mode = models.CharField(max_length = 20)
    

class OrderProducts(models.Model):
    order_id = models.ForeignKey(Order, on_delete= models.SET_NULL, null = True,blank = True) 
    user1 =  models.ForeignKey(Customuser, on_delete= models.SET_NULL, null = True,blank = True) 
    product_id = models.ForeignKey(Product, on_delete= models.SET_NULL, null = True,blank = True)  
    quantity = models.PositiveIntegerField(default = 0)
    amount =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank = True,null = True)
    status = models.CharField(max_length = 30,blank = True,null = True)
    address1 = models.ForeignKey(Address, on_delete= models.SET_NULL,null = True,blank = True) 
    delivery_date = models.DateField(null=True,blank = True)
    
    
    # def save(self, *args, **kwargs):
        
    #         self.delivery_date = self.order_id.order_date   +  timedelta(days=10)
            
    #         super().save(*args, **kwargs)
@receiver(pre_save, sender=OrderProducts)
def update_delivery_date(sender, instance, **kwargs):
    if not instance.delivery_date:
        instance.delivery_date = instance.order_id.order_date + timedelta(days=10)