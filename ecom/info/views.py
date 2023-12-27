from django.shortcuts import render,redirect
from home.models import Customuser
from django.core.mail import send_mail

# Create your views here.


def contact_us(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        return render(request, 'contact.html',{'username':username.first_name})
        
        
    return render(request, 'contact.html')

def about_us(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        return render(request, 'about.html',{'username':username.first_name})
        
        
    return render(request, 'about.html')







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