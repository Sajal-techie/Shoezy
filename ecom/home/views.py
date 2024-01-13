from django.shortcuts import render,redirect
from . models import Customuser
from django.utils import timezone
from django.contrib import messages
from . signals import send_otp
from django.views.decorators.cache import never_cache
from productmanagement.models import Product,ProductImages
from categorymanagement.models import Brand
from cart.models import *


@never_cache
def home(request):
    try:
        products = Product.objects.filter(is_listed = True, brand_id__is_listed = True).order_by('-id')[:8]
        brands = Brand.objects.filter(is_listed = True)

        context = {
            'product' : products,
            'brand' : brands,
        }
        if 'users' in request.session:
            usm = request.session.get('users')
            
            try:
                username = Customuser.objects.get(email = usm)
            except:
                username = None
                
            username.otp = None 
            username.save()

            
            if not username.is_blocked:  
                # getting cart count and wishlist count for displaying badge
                
                cartcount = Cart.objects.filter(user_id = username).count()
                wishcount = Wishlist.objects.filter(user_id = username).count()
                        
                wishlist1 = []
                wishitems = Wishlist.objects.filter(user_id = username)
                for j in wishitems:
                    wishlist1.append(j.product_id.id)
                    
                return render (request, 'home1.html',{'username': username.first_name,
                                                    'product' : products, 
                                                    'brand' : brands,
                                                    'cartcount':cartcount,
                                                    'wishcount':wishcount,
                                                    'wishlist1':wishlist1
                                                    })
            else:
                # if users are blocked sessions are cleared and redirect to login 
                
                if 'users' in request.session:
                    del request.session['users']
                messages.error(request,'you are blocked ')
                return redirect('login')
        
    except Exception as e:
        print(e)
    return render (request, 'home1.html',context)


@never_cache
def login(request):
    if 'users' in request.session:
        return redirect('home')
    try:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            try:
                user  = Customuser.objects.get(email = email,password = password )
            except Customuser.DoesNotExist or Customuser.MultipleObjectsReturned:
                user = None
            if user is not None:
                if user.is_blocked == True:
                    messages.error(request,'You are blocked ')
                    return redirect('login')
                
                if  user.is_verified == True:
                    request.session['users'] = email
                    return redirect('home')
                else:
                    # user need to verify if not verified earlier (otp sended again)
                    messages.error(request,'verify your mail')
                    send_otp(user)
                    return redirect('verifyreg',id = user.id)
            else:
                messages.error(request,"invalid username or password")
                return redirect('login')
            
    except Exception as e:
        print(e)
           
    return render(request, 'login/login.html')


@never_cache
def register(request):
    if 'users' in request.session:
        return redirect('home')
    
    try:
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password  = request.POST['password']
            confpassword = request.POST['password1']
            date_joined  = timezone.now().date()
            
            if Customuser.objects.filter(email = email).exists():
                messages.error(request,"Email already exists you can login ")
                return redirect('login')
            
            if len(password) < 6 and len(confpassword) < 6:
                messages.error(request," Password length too short minimum 6 chararcters")
                return redirect('register')
            
            if password != confpassword:
                messages.error(request,"Passwords must be same")
                return redirect('register')
            
            user  = Customuser(first_name = fname,last_name = lname,email = email,password = password,datejoined=date_joined)
            user.save()

            return redirect('verifyreg',id = user.id )
        
    except Exception as e:
        print(e)
        
    return render(request, 'login/register.html')


@never_cache
def verifyreg(request,id):
    if 'users' in request.session:
        return redirect('home')
    try:
        if id:
            context={
                    'userid':id
                }
            if request.method == 'POST':
                user_otp = request.POST['otp']
                
                try:
                    tb_user = Customuser.objects.get(id = id)
                except Customuser.DoesNotExist:
                    tb_user = None
                    
                if tb_user.otp == user_otp:
                    if tb_user.is_verified:
                        return render(request, 'login/reset_pass.html',{'id':id})
                    
                    else:
                        tb_user.is_verified = True
                        tb_user.save()
                        request.session['users'] = tb_user.email
                        return redirect('home')
                else:
                    messages.error(request,"Invalid otp Try again!")
                    return redirect('verifyreg',id = id)

            return render(request, 'login/verifyreg.html',context)
        
    except Exception as e:
        print(e)
        
    return redirect('register')


@never_cache
def resendotp(request,id):
    try:
        user = Customuser.objects.get(id = id)
    except Customuser.DoesNotExist:
        user = None
        
    send_otp(user)
    return redirect('verifyreg',id = user.id)


def forget_pass(request):
    try:
        if request.method == "POST":
            email = request.POST['email']
            try:
                user1 = Customuser.objects.get(email = email)
            except:
                messages.error(request, "enter registered email")
                return redirect('login')
            
            if user1 is not None:
                messages.success(request,"Confrim your email using the OTP")
                send_otp(user1)
                return redirect('verifyreg',id = user1.id)
            
    except Exception as e:
        print(e)
        
    messages.error(request,"enter registered mail")
    return redirect('login')
            
    
# after forget password (before login)
def reset_pass(request,id):
    try:
        if request.method == 'POST':
            pass1 = request.POST['password']
            pass2 = request.POST['password1']
            
            if len(pass1) < 6:
                messages.error(request,"password must be atleast 6 character ")
                return redirect('reset_pass',id)
                
            if pass1 != pass2:
                messages.error(request, "passwords must be same")
                return redirect('reset_pass',id)
            try:
                user2 = Customuser.objects.get(id=id)
            except Customuser.DoesNotExist:
                user2 = None
            
            if user2 is not None:
                user2.password = pass1
                user2.save()
                messages.success(request,"password resetted successfully now you can login ")
                return redirect('login')
            
            return redirect('login')
        
    except Exception as e:
        print(e)
        
    return render(request, 'login/reset_pass.html',{'id':id})         


def logout(request):
    if 'users' in request.session:
        del request.session['users']
    return redirect('home')


def page_not_found(request):
    return render(request, 'page_not_found.html',status=404) 
