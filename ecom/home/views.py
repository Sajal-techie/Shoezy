from django.shortcuts import render,redirect
from . models import Customuser
from django.utils import timezone
from django.contrib import messages
from . signals import send_otp
from django.views.decorators.cache import never_cache
from productmanagement.models import Product,ProductImages
from categorymanagement.models import Brand



# Create your views here.
@never_cache
def home(request):
    products = Product.objects.filter(is_listed = True, brand_id__is_listed = True).order_by('-id')[:8]
    brands = Brand.objects.filter(is_listed = True)
    # multiple = ProductImages.objects.all()
    
    context = {
        'product' : products,
        'brand' : brands,
    }
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        username.otp = None
        username.save()

        
        if not username.is_blocked:  
            return render (request, 'home1.html',{'username': username.first_name,'product' : products, 'brand' : brands,})
        else:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            return redirect('login')
    return render (request, 'home1.html',context)


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

            
            return redirect('login')
        
    return render(request, 'login/login.html')

@never_cache
def register(request):
    if 'users' in request.session:
        return redirect('home')
    
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password  = request.POST['password']
        confpassword = request.POST['password1']
        date_joined  = timezone.now().date()
        
        if Customuser.objects.filter(email = email).exists():
            messages.error(request," email already exists you can login ")
            return redirect('login')
        
        if len(password) < 6:
            messages.error(request," password length too short minimum 6 chararcters ")
            return redirect('register')
        
        if password != confpassword:
            messages.error(request," passwords must be same ")
            return redirect('register')
        
        user  = Customuser(first_name = fname,last_name = lname,email = email,password = password,datejoined=date_joined)
        user.save()
        
        
        
        
        return redirect('verifyreg',id = user.id )
        
    return render(request, 'login/register.html')


@never_cache
def verifyreg(request,id):
    if 'users' in request.session:
        return redirect('home')
    if id:
        context={
                'userid':id
            }
        if request.method == 'POST':
            user_otp = request.POST['otp']
            tb_user = Customuser.objects.get(id = id)
            if tb_user.otp == user_otp:
                if tb_user.is_verified:
                    return render(request, 'login/reset_pass.html',{'id':id})
                
                else:
                    tb_user.is_verified = True
                    tb_user.save()
                    request.session['users'] = tb_user.email
                    return redirect('home')
            else:
                messages.error(request,"invalid otp")
                return redirect('verifyreg',id = id)

        return render(request, 'login/verifyreg.html',context)
    return redirect('register')

@never_cache
def resendotp(request,id):
    user = Customuser.objects.get(id = id)
    send_otp(user)
    return redirect('verifyreg',id = user.id)


def forget_pass(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user1 = Customuser.objects.get(email = email)
        except:
            messages.error(request, "enter registered email")
            return redirect('login')
        
        if user1 is not None:
            messages.success(request,"confrim your mail")
            send_otp(user1)
            return redirect('verifyreg',id = user1.id)
        
        messages.error(request,"enter registered mail")
        
    return redirect('login')
            
    
    
def reset_pass(request,id):
    if request.method == 'POST':
        pass1 = request.POST['password']
        pass2 = request.POST['password1']
        
        if len(pass1) < 6:
            messages.error(request,"password must be atleast 6 character ")
            return redirect('reset_pass',id)
            
            
        if pass1 != pass2:
            messages.error(request, "passwords must be same")
            return redirect('reset_pass',id)

        user2 = Customuser.objects.get(id=id)
        
        if user2 is not None:
            user2.password = pass1
            user2.save()
            messages.success(request,"password resetted successfully")
            return redirect('login')
        
        return redirect('login')
        
    return render(request, 'login/reset_pass.html',{'id':id})         


def logout(request):
    if 'users' in request.session:
        del request.session['users']
    return redirect('home')