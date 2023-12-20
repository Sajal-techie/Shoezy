from django.shortcuts import render,redirect
from . models import Customuser
from django.utils import timezone
from django.contrib import messages
from . signals import send_otp
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        username.otp = None
        username.save()
        if not username.is_blocked: 
            return render (request, 'home1.html',{'username': username.first_name})
        else:
            if 'users' in request.session:
                request.session.flush()
            messages.error(request,'you are blocked ')
            return redirect('login')
    return render (request, 'home1.html')


@never_cache
def login(request):
    if 'users' in request.session:
        return redirect('home')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user  = Customuser.objects.get(email = email,password = password )
        except Customuser.DoesNotExist or Customuser.MultipleObjectsReturned:
            user = None
        if user is not None:
            if user.is_blocked == True:
                messages.error(request,'you are blocked ')
                return redirect('login')
            
            if  user.is_verified == True:
                request.session['users'] = email
                return redirect('home')
            else:
                messages.error(request,'verify your mail')
                send_otp(user)
                return redirect('verifyreg',id = user.id)
        else:
            messages.error(request,"invalid username or password")
            print('redirected')
            return redirect('login')
    print('return')
    return render(request, 'login/login.html')

@never_cache
def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password  = request.POST['password']
        confpassword = request.POST['password1']
        date_joined  = timezone.now().date()
        if Customuser.objects.filter(email = email).exists():
            messages.error(request," email already exists you can login ")
            return redirect(login)
        user  = Customuser(first_name = fname,last_name = lname,email = email,password = password,datejoined=date_joined)
        user.save()
        
        
        return redirect('verifyreg',id = user.id )
        
    return render(request, 'login/register.html')

@never_cache
def verifyreg(request,id):
    context={
            'userid':id
        }
    if request.method == 'POST':
        user_otp = request.POST['otp']
        tb_user = Customuser.objects.get(id = id)
       
        print(tb_user.otp,user_otp , tb_user.is_verified)
        if tb_user.otp == user_otp:
            tb_user.is_verified = True
            tb_user.save()
            request.session['users'] = tb_user.email
            return redirect('home')
        else:
            messages.error(request,"invalid otp")
            return redirect('verifyreg',id = id)

    return render(request, 'login/verifyreg.html',context)

@never_cache
def resendotp(request,id):
    user = Customuser.objects.get(id = id)
    send_otp(user)
    return redirect('verifyreg',id = user.id)


def logout(request):
    if 'users' in request.session:
        request.session.flush()
    return redirect('home')