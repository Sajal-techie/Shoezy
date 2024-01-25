from django.shortcuts import render, redirect
from home.models import Customuser
from cart.models import *
from django.core.mail import send_mail
from django.contrib import messages

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
        return render(request, "contact.html", {"username": username.first_name})

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
        return render(request, "about.html", {"username": username.first_name})

    return render(request, "about.html")


def terms(request):
    return render(request, "terms.html")


def send_message(request):
    pass
    # if request.method == "POST":
    #     name = request.POST['name']
    #     email = request.POST['email']
    #     to_email = [email]
    #     subjects = request.POST['subject']
    #     from_email = "shoezyofficials@gmail.com"
    #     message = f"Thanks for contacting us {name} for {subjects}'\n' continue shopping "
    #     subject = "Shoezy Customer support "
    #     send_mail(subject,message,from_email,to_email)
    #     return redirect('contact_us')

    # return redirect('contact_us')
