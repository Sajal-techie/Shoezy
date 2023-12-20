from django.db import models
# from django.utils import timezone
# Create your models here.

class Customuser(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField()
    datejoined = models.DateField()
    password = models.CharField(max_length = 255)
    is_verified = models.BooleanField(default = False)
    is_listed = models.BooleanField(default = True)
    otp = models.CharField(max_length = 6, null = True, blank = True)
