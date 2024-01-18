from django.shortcuts import render,redirect
from .models import *
from .forms import Adressform
from home.models import Customuser
from order_management.models import *
from django.views.decorators.cache import never_cache,cache_control
from django.contrib import messages
from cart.models import *
from django.db.models import Q
from django.utils import timezone
from datetime import date


def view_profile(request):
    try:
        if 'users' in request.session:
            usm = request.session.get('users')
            try:
                username = Customuser.objects.get(email = usm)
            except Customuser.DoesNotExist:
                username = None
                
            if username.is_blocked:
                if 'users' in request.session:
                    del request.session['users']
                messages.error(request,'you are blocked ')
                return redirect('login') 
            try:
                addressess = Address.objects.filter(Q(user = username) & Q(is_available= True))
                cartcount = Cart.objects.filter(user_id = username).count()
                
                try:
                    wallet = Wallet.objects.get(user_id = username)
                except Wallet.DoesNotExist:
                    wallet = None
                    
            except Exception as e:
                print(e)
                
            context = {
                'username':username,
                'address':addressess,
                'cartcount':cartcount,
                'wallet':wallet
            }
            wishcount = Wishlist.objects.filter(user_id = username).count()
            context['wishcount']=wishcount
            
            return render(request, 'profile/user_details.html',context)
        
    except Exception as e:
        print(e)
        return redirect('home')
    
    return redirect('login')
    
    
@never_cache
def edit_profile(request,id):
    try: 
        try:
            username = Customuser.objects.get(id = id)
        except Customuser.DoesNotExist:
            username = None
        try:
            cartcount = Cart.objects.filter(user_id = username).count()
        except Exception as e:
            print(e)
            
        context = {
            'username':username,
            'cartcount':cartcount
        }
        wishcount = Wishlist.objects.filter(user_id = username).count()
        context['wishcount']=wishcount
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            number = request.POST['number']
            gender = request.POST['gender']
            dob = request.POST['dob']
            
            # check if the dob is null or not and change the dob
            if dob != "" :
                date_obj = date.fromisoformat(dob)  
                eighteen = timezone.now().date() - timezone.timedelta(365 * 18) 
                if date_obj >  eighteen:
                    messages.error(request,'You do not meet the age requirements.(minimum 18 years old)')
                    return redirect('edit_profile',id)
                else:
                    username.dob = date_obj
                    
            if not number == "" and len(number) != 10:
                messages.error(request,'Enter valid number')
                return redirect('edit_profile',id)

            username.first_name = fname
            username.last_name = lname
            username.number = number
            username.gender = gender
            username.save()
            return redirect('view_profile')
        return render(request, 'profile/edit_profile.html',context)
    
    except Exception as e:
        print(e)
        
    return redirect('view_profile')


# reset password from profile after logging in
@never_cache
@cache_control(no_store=True, no_cache = True, must_revalidate=True,max_age=0)
def reset_password(request):
    try:
        if 'users' in request.session:
            usm = request.session.get('users')
            try:
                username = Customuser.objects.get(email = usm)
            except Customuser.DoesNotExist:
                username = None
                
            cartcount = Cart.objects.filter(user_id = username).count()
            context = {
                'username' : username,
                'cartcount':cartcount
            }
            wishcount = Wishlist.objects.filter(user_id = username).count()
            context['wishcount']=wishcount
            if request.method == 'POST':
                old = request.POST['old_pass']
                new = request.POST['new_pass']
                new1 = request.POST['new_pass1']
                if username.password == old:
                    if len(new) < 6:
                        messages.error(request,'password must be more than 6 characters')
                        return redirect('reset_password')
                    if new != new1:
                        messages.error(request,'passwords must be equal')
                        return redirect('reset_password')
                    
                    username.password = new
                    username.save()
                    return redirect('view_profile')
                else:
                    messages.error(request, 'incorrect password')
                    return redirect('reset_password')
                    
            return render (request, 'profile/reset_password.html',context)
        
    except Exception as e:
        print(e)
        return redirect('view_profile')
    return redirect('login')

def add_address(request):
    try:
        if 'users' in request.session:
            usm = request.session.get('users')
            try:
                username = Customuser.objects.get(email = usm)
            except Customuser.DoesNotExist:
                username = None
                
            if request.method == 'POST':
                try:
                    form = Adressform(request.POST)
                except Exception as e:
                    print(e)
                    
                if form.is_valid():
                    address = form.save(commit = False)
                    
                    if len(address.number) != 10:
                        messages.error(request, 'Enter valid number')
                        return redirect('add_address')
                    
                    if address.pincode >= 999999:
                        messages.error(request,'enter valid pincode')
                        return redirect('add_address')
                    
                    address.user = username
                    address.save()
                    next_url = request.GET.get('next', None)

                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('home')
            else: 
                form = Adressform()
            return render(request,'profile/add_address.html',{'form':form,'username':username})
    except Exception as e:
        print(e)
        return redirect('view_profile')
    return redirect('login')


def edit_address(request,id):
    try:
        existing_address = Address.objects.get(id=id)
    except Address.DoesNotExist:
        existing_address = None
        
    if request.method == 'POST':
        form = Adressform(request.POST, instance=existing_address)
        if form.is_valid():
            address = form.save(commit = False)
                    
            if len(address.number) != 10:
                messages.error(request, 'Enter valid number')
                return redirect('add_address')
                    
            if address.pincode >= 999999:
                messages.error(request,'enter valid pincode')
                return redirect('add_address')
                    
            address.save()
            return redirect('view_profile') 
    else:
        form = Adressform(instance=existing_address)

    return render(request, 'profile/edit_address.html', {'form': form, 'address': id})


def delete_address(request,id):
    try:
        address = Address.objects.get(id = id)
    except Address.DoesNotExist:
        address = None
        
    address.is_available = False
    address.save()
    return redirect('view_profile')


def order_history(request):
    try:
        if 'users' in request.session:
            usm = request.session.get('users')
            username = Customuser.objects.get(email = usm)
            if username.is_blocked:
                if 'users' in request.session:
                    del request.session['users']
                messages.error(request,'you are blocked ')
                return redirect('login') 
            try:
                order_items = OrderProducts.objects.filter(user1 = username).order_by('-id')
                cartcount = Cart.objects.filter(user_id = username).count()
            except Exception as e:
                print(e)
                
            context = {
                'order_items': order_items,
                'username':username,
                'cartcount':cartcount
            }
            wishcount = Wishlist.objects.filter(user_id = username).count()
            context['wishcount']=wishcount
            
            return render(request, 'profile/order_history.html',context) 
        
    except Exception as e:
        print(e)
        return redirect('home')
    return redirect('login')

def track_order(request,id):
    try:
        if 'users' in request.session:
            usm = request.session.get('users')
            username = Customuser.objects.get(email = usm)
            try:
                order_items = OrderProducts.objects.get(id = id)
            except OrderProducts.DoesNotExist:
                order_items = None
                
            cartcount = Cart.objects.filter(user_id = username).count()
            tracking_steps = [
                {'description': 'ordered'},
                {'description': 'shipped'},
                {'description': 'out for delivery'},
                {'description': 'delivered'},
            ]

            current_status = order_items.status
            current_step_index = next((i for i, step in enumerate(tracking_steps) if step['description'] == current_status), None)
            previous_steps = tracking_steps[:current_step_index + 1 ] 
            context = {
                'order': order_items,
                'tracking_steps': tracking_steps,
                'previous_steps': previous_steps,
                'username':username,
                'cartcount':cartcount,
            }
            wishcount = Wishlist.objects.filter(user_id = username).count()
            context['wishcount']=wishcount
            return render(request, 'profile/track_order.html',context)
        
    except Exception as e:
        print(e)
        return redirect('order_history')
    return redirect('login')


def cancel_order(request,id):
    try:
        if 'users' in request.session:
            usm = request.session.get('users')
            username = Customuser.objects.get(email = usm)
            try:
                current_order = OrderProducts.objects.get(id=id)
            except OrderProducts.DoesNotExist:
                current_order = None
                
            if request.method == 'POST':
                reason = request.POST['reason']
            
                if current_order.status != 'delivered':
                    current_order.status = 'cancelled'
                    current_order.reason = reason
                    current_order.delivery_date =  timezone.now()
                    current_order.save()
                    current_order.product.stock = current_order.product.stock + current_order.quantity
                    current_order.product.save()
                    
                    if current_order.order_id.payment_mode != 'Cash on delivery':
                        try:
                            wallet = Wallet.objects.get(user_id = username)
                        except Wallet.DoesNotExist:
                            wallet = None
                        if wallet is not None:
                            wallet.amount = wallet.amount + current_order.amount
                            wallet.save()
                    
                    return redirect('order_history')
            return redirect('order_history')
        
    except Exception as e:
        print(e)
        return redirect('order_history')
    
    return redirect('login')


def view_order_details(request,id):
    try:
        if 'users' in request.session:
            usm = request.session.get('users')
            username = Customuser.objects.get(email = usm)
            try:
                order = OrderProducts.objects.get(id = id )
            except OrderProducts.DoesNotExist:
                order = None
                
            context = {
                'username': username,
                'order_item': order 
            }
            return render(request, 'profile/view_order_details.html',context)
    except Exception as e:
        print(e)
        return redirect('order_history')
    return redirect('login')


