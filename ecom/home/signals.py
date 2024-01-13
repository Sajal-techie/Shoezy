
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Customuser
import random


def genotp():
    return str(random.randint(100000,999999))


@receiver(post_save, sender = Customuser)
def send_otp_signal(sender, instance,created, **kwargs):

    if created and instance.is_verified == False:
        send_otp(instance)    
        
        
def send_otp(user):
        i  = 0
        otp1 = genotp()
        otp1 = int(otp1)
        user.otp = otp1   
        user.save()
        subject = 'Welcome to shopzy this is for otp verification'
        message = f"your otp is: {otp1}"
        from_email = "shoezyofficials@gmail.com"
        to_email = [user.email]
        send_mail(subject,message,from_email,to_email)
     
