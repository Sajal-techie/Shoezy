from django.shortcuts import render, redirect
from home.models import Customuser
from cart.models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
# Create your views here.


def contact_us(request):
    if "users" in request.session:
        usm = request.session.get("users")
        username = Customuser.objects.get(email=usm)
        if username.is_blocked:
            if "users" in request.session:
                del request.session["users"]
            messages.error(request, "you are blocked ")
            return redirect("login")
        return render(request, "contact.html")

    return render(request, "contact.html")


def about_us(request):
    if "users" in request.session:
        usm = request.session.get("users")
        username = Customuser.objects.get(email=usm)
        if username.is_blocked:
            if "users" in request.session:
                del request.session["users"]
            messages.error(request, "you are blocked ")
            return redirect("login")
        return render(request, "about.html")

    return render(request, "about.html")


def terms(request):
    return render(request, "terms.html")

# message us 
def send_message(request):
    if request.method == "POST":
        try:
            name = request.POST['name']
            email = request.POST['email']
            to_email = [email]
            subjects = request.POST['subject']
            from_email = settings.EMAIL_HOST_USER
            message = f"Thanks for contacting us '{name}' for '{subjects}' \nContinue shopping with US "
            subject = "Shoezy Customer support "
            send_mail(subject,message,from_email,to_email)
            
        except Exception as e:
            print(e)
            
        return redirect('contact_us')

    return redirect('contact_us')
