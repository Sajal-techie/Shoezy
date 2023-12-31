from django.shortcuts import render,redirect
from .models import Address
from .forms import Adressform
from home.models import Customuser
from order_management.models import *
from django.views.decorators.cache import never_cache
from django.contrib import messages
# Create your views here.

def view_profile(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        addressess = Address.objects.filter(user = username)
        context = {
            'username':username,
            'address':addressess,
            
            
        }
        return render(request, 'profile/user_details.html',context)

@never_cache
def edit_profile(request,id):
    username = Customuser.objects.get(id = id)
    context = {
        'username':username
    }
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        number = request.POST['number']
        gender = request.POST['gender']
        dob = request.POST['dob']
        username.first_name = fname
        username.last_name = lname
        username.number = number
        username.gender = gender
        username.dob = dob
        username.save()
        return redirect('view_profile')
    return render(request, 'profile/edit_profile.html',context)


@never_cache
def reset_password(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        context = {
            'username' : username
        }
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


def view_address(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        address = Address.objects.filter(user = username)
        return render(request,'profile/address.html',{'address':address,'username':username})



def add_address(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        if request.method == 'POST':
            form = Adressform(request.POST)
            print(form.errors)
            if form.is_valid():
                address = form.save(commit = False)
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


def delete_address(request,id):
    address = Address.objects.get(id = id)
    address.delete()
    return redirect('view_profile')


def order_history(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        # orders= Order.objects.filter(user = username)
        order_items = OrderProducts.objects.filter(user1 = username).order_by('-id')
        
        context = {
            # 'orders':orders,
            'order_items': order_items,
            'username':username
        }

        
        return render(request, 'profile/order_history.html',context)


def track_order(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        order_items = OrderProducts.objects.get(id = id)
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
            'username':username
        }
        return render(request, 'profile/track_order.html',context)
    
    return redirect('login')

def cancel_order(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        
        current_order = OrderProducts.objects.get(id=id)
        
        if current_order.status != 'delivered':
            current_order.status = 'cancelled'
            current_order.save()
            
            return redirect('order_history')
        
        return redirect('order_history')
    
    return redirect('login')
    