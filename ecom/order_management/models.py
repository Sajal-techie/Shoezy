from django.db import models
from home.models import Customuser
from user_profile.models import *
from productmanagement.models import *
from datetime import timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver
from coupon.models import *
# Create your models here.
 
class Order(models.Model):
    user = models.ForeignKey(Customuser, on_delete= models.SET_NULL, null = True,blank = True) 
    address = models.ForeignKey(Address, on_delete= models.SET_NULL,null = True,blank = True) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank = True,null = True)
    order_date = models.DateField(auto_now_add = True)
    payment_mode = models.CharField(max_length = 20)
    coupon_applied = models.BooleanField(default = False,null = True)
    coupon_id = models.ForeignKey(Coupen, on_delete = models.SET_NULL, null = True)
    og_amount = models.FloatField( null = True,blank = True)
    

class OrderProducts(models.Model):
    order_id = models.ForeignKey(Order, on_delete= models.SET_NULL, null = True,blank = True) 
    user1 =  models.ForeignKey(Customuser, on_delete= models.SET_NULL, null = True,blank = True) 
    product = models.ForeignKey(ProductVariant, on_delete= models.SET_NULL, null = True,blank = True )
    size = models.IntegerField() 
    quantity = models.PositiveIntegerField(default = 0)
    amount =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank = True,null = True)
    status = models.CharField(max_length = 30,blank = True,null = True)
    address1 = models.ForeignKey(Address, on_delete= models.SET_NULL,null = True,blank = True) 
    delivery_date = models.DateField(null=True,blank = True)
    reason = models.TextField(null = True,blank = True)
    
    
@receiver(pre_save, sender=OrderProducts)
def update_delivery_date(sender, instance, **kwargs):
    if not instance.delivery_date:
        instance.delivery_date = instance.order_id.order_date + timedelta(days=10)
        
        
class Returns(models.Model):
    order = models.ForeignKey(OrderProducts, on_delete = models.SET_NULL,null = True)
    user = models.ForeignKey(Customuser, on_delete = models.SET_NULL, null = True)
    reason = models.TextField(null = True,blank = True) 
    request_date = models.DateField(auto_now_add = True,null = True)
    return_date = models.DateField(null = True,blank = True) 