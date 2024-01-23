from django.db import models
import string
import random

class Customuser(models.Model):
    CATEGORY_CHOICES = [ ('men' ,'Men'),
                ('women', 'Women'),
                ('others', 'Others')]
    first_name = models.CharField(max_length = 255,null = True)
    last_name = models.CharField(max_length = 255,null = True)
    email = models.EmailField(unique = True)
    datejoined = models.DateField(auto_now_add = True,null = True)
    password = models.CharField(max_length = 255)
    is_verified = models.BooleanField(default = False)
    is_listed = models.BooleanField(default = True)
    is_blocked = models.BooleanField(default = False)
    otp = models.CharField(max_length = 6, null = True, blank = True)
    number = models.CharField(max_length = 20, null = True, blank = True)
    dob = models.DateField(null = True, blank = True)
    gender = models.CharField(choices =CATEGORY_CHOICES, null= True,blank = True )
    referal_code = models.CharField(max_length = 10,null = True)
    
    
    def save(self, *args, **kwargs):
        if not self.referal_code:
            self.referal_code = self.generate_referral_code()

        super().save(*args, **kwargs)

    def generate_referral_code(self, length=8):
        characters = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(characters) for i in range(length))
        return code
     
    
    def __str__(self) -> str:
        return f'{self.first_name}  {self.last_name}' 