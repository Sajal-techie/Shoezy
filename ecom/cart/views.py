from django.shortcuts import render,redirect
from django.contrib import messages
from home.models import Customuser
from productmanagement.models import Product,ProductImages
from . models import Cart
from user_profile.models import Address
from order_management.models import *

# Create your views here.


def cart(request):   
    
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)        
        cart_items = Cart.objects.filter(user_id = username).select_related('product_id__brand').order_by('-id')
        total = sum(i.sub_total for i in cart_items)
        
        context = {
            'username': username,
            'cart_item': cart_items,
            'total':total
        }
        
        if not username.is_blocked:      
            return render(request, 'cart/cart.html', context)
        else:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            
            return redirect('login')
    
    messages.error(request,'you need to login')
    return redirect('login')





def addto_cart(request,p_id):
    if 'users' in request.session:
        context={}
        usm = request.session.get('users')
        user2 = Customuser.objects.get(email = usm)
        product = Product.objects.get(id = p_id)
        # cart_item = Cart.objects.get(user_id = user2,product_id= product)
        # if cart_item is None:
        if product.quantity > 0:
                Cart.objects.create( user_id = user2 ,product_id = product,quantity = 1)
                # is_in_cart = check_cart(user2,product.id)
                # context={
                #     'is_in_cart':is_in_cart
                # }
                
        next_url = request.GET.get('next', '/')
        return redirect(next_url,context)
    messages.error(request,'you need to login')
    return redirect('login')
        
        
        
def check_cart(user,product_id):
    is_in_cart = Cart.objects.filter(user_id = user, product_id=product_id).exists()
    return is_in_cart    
  
        
def add_quantity(request,id):
    item = Cart.objects.get(id=id)
    # product = Product.objects.get(id = item.product_id)
    if item.quantity < item.product_id.quantity:
        item.quantity = item.quantity + 1
        item.sub_total = item.product_id.selling_price * item.quantity
        item.save()
    return redirect('cart')
    

def rem_quantity(request,id):
    item= Cart.objects.get(id=id)
    if item.quantity > 1:
        item.quantity = item.quantity - 1
        item.sub_total = item.product_id.selling_price * item.quantity
        item.save()
    return redirect('cart')
    
    
def remove_cart(request,id):
    remove_item= Cart.objects.get(id = id)
    remove_item.delete()
    return redirect('cart')


def checkout(request):
    if 'users' in request.session:
            usm = request.session.get('users')
            username = Customuser.objects.get(email = usm)
            address = Address.objects.filter(user = username.id)
            cart_items = Cart.objects.filter(user_id = username.id).select_related('product_id__brand')
            total = sum(i.sub_total for i in cart_items)
            context = {
                'address':address,
                'cart_items':cart_items,
                'username' :username,
                'total':total
            }
            if request.method == 'POST':
                adress1 = request.POST.get('address',None)
                if not adress1:
                    messages.error(request,'add address for delivery')
                    return redirect('checkout')
                payment = request.POST['payment']
                adress =  Address.objects.get(id = adress1)
                current_order = Order.objects.create(user = username, address = adress,total = total,payment_mode = payment)
                for i in cart_items:
                    obj = OrderProducts(order_id = current_order,user1 = username,product_id = i.product_id ,address1 = adress,quantity = i.quantity,amount = i.sub_total,status = 'ordered')
                    if obj.product_id.quantity >= 1: 
                        obj.product_id.quantity = obj.product_id.quantity - obj.quantity
                        obj.product_id.save()
                    else:
                        messages.error(request, 'out of stock')
                        return redirect('checkout')
                    obj.save()
                    i.delete()
            
                return redirect('confirm',current_order.id)
            
              
            return render(request, 'cart/checkout.html',context)
    


def confirm(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        orders = Order.objects.get(id = id)
        order_items = OrderProducts.objects.filter(order_id = id)
        context = {
            'username':username,
            'orders' : orders,
            'order_items': order_items
        }
        
        return render(request, 'cart/confirm.html',context)
    
    return redirect('login')