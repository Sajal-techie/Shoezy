
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Customuser

import random
def genotp():
    return str(random.randint(100000,999999))


@receiver(post_save, sender = Customuser)
def send_otp_signal(sender, instance,created, **kwargs):

    print('hi')
    if created and instance.is_verified == False:
        send_otp(instance)
        print("called otp send functions")
        # otp1 = genotp()
        # otp1 = int(otp1)
        # instance.otp = otp1
        # print(otp1)
        # instance.save()
        # subject = 'Welcome to shopzy this is for otp verification'
        # message = f"your otp is: {otp1}"
        # from_email = "shoezyofficials@gmail.com"
        # to_email = [instance.email]
        # send_mail(subject,message,from_email,to_email)
        
def send_otp(user):
        i  = 0
        print("function worked ")
        otp1 = genotp()
        otp1 = int(otp1)
        user.otp = otp1
        print(otp1)       
        user.save()
        subject = 'Welcome to shopzy this is for otp verification'
        message = f"your otp is: {otp1}"
        from_email = "shoezyofficials@gmail.com"
        to_email = [user.email]
        send_mail(subject,message,from_email,to_email)
     
    # else:
    #     print('elsecase')
    #     otp1 = genotp()
    #     otp1 = int(otp1)
    #     instance.otp = otp1
    #     print(otp1)
    #     instance.save()
    #     subject = 'Welcome to shopzy this is for otp verification'
    #     message = f"your otp is: {otp1}"
    #     from_email = "shoezyofficials@gmail.com"
    #     to_email = [instance.email]
    #     send_mail(subject,message,from_email,to_email)
# def send_otp(email,otp1):
    # otp1 = int(otp1)
    # print(otp1)
    # subject = 'Welcome to shopzy this is for otp verification'
    # message = f"your otp is: {otp1}"
    # from_email = "shoezyofficials@gmail.com"
    # to_email = [email]
    # send_mail(subject,message,from_email,to_email)