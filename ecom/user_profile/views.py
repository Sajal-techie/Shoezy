from django.shortcuts import render,redirect
from .models import Address
from .forms import Adressform
from home.models import Customuser
from order_management.models import *
from django.views.decorators.cache import never_cache,cache_control
from django.contrib import messages
from cart.models import *
from django.db.models import Q
# Create your views here.

def view_profile(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        if username.is_blocked:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            return redirect('login') 
        addressess = Address.objects.filter(Q(user = username) & Q(is_available= True))
        cartcount = Cart.objects.filter(user_id = username).count()
        context = {
            'username':username,
            'address':addressess,
            'cartcount':cartcount,
        }
        wishcount = Wishlist.objects.filter(user_id = username).count()
        context['wishcount']=wishcount
        return render(request, 'profile/user_details.html',context)

@never_cache
def edit_profile(request,id):
    username = Customuser.objects.get(id = id)
    cartcount = Cart.objects.filter(user_id = username).count()
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
        if len(number) != 10:
            messages.error(request,'Enter valid number')
            return redirect('edit_profile',id)
        username.first_name = fname
        username.last_name = lname
        username.number = number
        username.gender = gender
        username.dob = dob
        username.save()
        return redirect('view_profile')
    return render(request, 'profile/edit_profile.html',context)

@never_cache
@cache_control(no_store=True, no_cache = True, must_revalidate=True,max_age=0)
def reset_password(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
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


# def view_address(request):
#     if 'users' in request.session:
#         usm = request.session.get('users')
#         username = Customuser.objects.get(email = usm)
#         address = Address.objects.filter(user = username)
#         return render(request,'profile/address.html',{'address':address,'username':username})



def add_address(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        if request.method == 'POST':
            form = Adressform(request.POST)
            print(form.errors)
            if form.is_valid():
                address = form.save(commit = False)
                if len(address.number) != 10:
                    messages.error(request, 'Enter valid number')
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


def edit_address(request,id):
    existing_address = Address.objects.get(id=id)
    if request.method == 'POST':
        form = Adressform(request.POST, instance=existing_address)
        if form.is_valid():
            form.save()
            return redirect('view_profile') 
    else:
        # Create a form instance and pre-fill with existing data
        form = Adressform(instance=existing_address)

    return render(request, 'profile/edit_address.html', {'form': form, 'address': id})


def delete_address(request,id):
    address = Address.objects.get(id = id)
    address.is_available = False
    address.save()
    return redirect('view_profile')


def order_history(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        if username.is_blocked:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            return redirect('login') 
        # orders= Order.objects.filter(user = username)
        order_items = OrderProducts.objects.filter(user1 = username).order_by('-id')
        cartcount = Cart.objects.filter(user_id = username).count()
        context = {
            # 'orders':orders,
            'order_items': order_items,
            'username':username,
            'cartcount':cartcount
        }
        wishcount = Wishlist.objects.filter(user_id = username).count()
        context['wishcount']=wishcount
        
        return render(request, 'profile/order_history.html',context)


def track_order(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        order_items = OrderProducts.objects.get(id = id)
        cartcount = Cart.objects.filter(user_id = username).count()
        tracking_steps = [
            {'description': 'ordered'},
            {'description': 'shipped'},
            {'description': 'out_for_delivery'},
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
    
    return redirect('login')

def cancel_order(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        
        current_order = OrderProducts.objects.get(id=id)
        if request.method == 'POST':
            reason = request.POST['reason']
        
            if current_order.status != 'delivered':
                current_order.status = 'cancelled'
                current_order.reason = reason
                current_order.delivery_date =  timezone.now()
                current_order.save()
                current_order.product.stock = current_order.product.stock + current_order.quantity
                current_order.product.save()
                 
                
                return redirect('order_history')
        
        return redirect('order_history')
    
    return redirect('login')
    
    
def view_order_details(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        order = OrderProducts.objects.get(id = id )
        context = {
            'username': username,
            'order_item': order 
        }
        return render(request, 'profile/view_order_details.html',context)
    return redirect('login')