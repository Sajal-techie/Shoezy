from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from home.models import Customuser
from productmanagement.models import *
from . models import *
from user_profile.models import Address
from order_management.models import *

# Create your views here.


def cart(request):   
    
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        if username.is_blocked:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            return redirect('login')       
        cart_items = Cart.objects.filter(user_id = username).select_related('product__product_id__brand').order_by('-id') 
        total = sum(i.sub_total for i in cart_items)
        cartcount = Cart.objects.filter(user_id = username).count()
        context = {
            'username': username,
            'cart_item': cart_items,
            'total':total,
            'cartcount':cartcount
        }
        wishcount = Wishlist.objects.filter(user_id = username).count()
        context['wishcount']=wishcount
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
        usm = request.session.get('users')
        user2 = Customuser.objects.get(email = usm)
        product = Product.objects.get(productvariant__id = p_id)
        size = request.GET.get('size',None)
        quantity = int(request.GET.get('quantity',None))
        try:
            product_size = ProductVariant.objects.get(product_id = product, size = size)  
        except ProductVariant.DoesNotExist:
            product_size = None
            
        if product_size is None:
            messages.error(request, 'Not available')
            return redirect('singleproduct',product.id) 
        
        if product_size.stock < quantity:
            messages.error(request,'out of Stock')
            return redirect('singleproduct',product.id) 
            
        if product_size.stock > 0:
            if  not Cart.objects.filter(user_id = user2, product = product_size, size = size).exists():
                 Cart.objects.create( user_id = user2 ,product = product_size, size = size, quantity = quantity ) 
            else:
                messages.error(request, 'Already in Cart')
        else:
            messages.error(request, 'Out of stock')
        return redirect('singleproduct',product.id)      
    messages.error(request,'you need to login')
    return redirect('login')
        
        
        
def check_cart(user,product_id):
    is_in_cart = Cart.objects.filter(user_id = user, product=product_id).exists()
    return is_in_cart    
  
def check_wishlist(user,product_id):
     is_in_wish = Wishlist.objects.filter(user_id = user,product_id=product_id).exists()
     return is_in_wish
        
def change_quantity(request):
    if request.method == 'POST':
        products_id = int(request.POST.get('products_id'))
        action = request.POST.get('action')
        item = Cart.objects.get(id=products_id)
        
        if action == 'plus':
            if item.quantity  < item.product.stock and item.quantity < 5:
                item.quantity = item.quantity  + 1        
        elif action =='minus':
            if item.quantity  > 1:
                item.quantity = item.quantity  - 1
                
        item.sub_total = item.product.product_id.selling_price * item.quantity
        item.save() 
        return JsonResponse({'status':"updated suucessfully"})
    

    
def remove_cart(request,id):
    remove_item= Cart.objects.get(id = id)
    remove_item.delete()
    return redirect('cart')


def checkout(request):
    if 'users' in request.session:
            usm = request.session.get('users')
            username = Customuser.objects.get(email = usm)
            address = Address.objects.filter(user = username.id,is_available = True).order_by('id')
            cart_items = Cart.objects.filter(user_id = username.id).select_related('product__product_id')
            total = sum(i.sub_total for i in cart_items)
            cartcount = Cart.objects.filter(user_id = username).count()

            context = {
                'address':address,
                'cart_items':cart_items,
                'username' :username,
                'total':total,
                'cartcount':cartcount
            }
            wishcount = Wishlist.objects.filter(user_id = username).count()
            context['wishcount']=wishcount
            if request.method == 'POST':
                adress1 = request.POST.get('address',None)
                if not adress1:
                    messages.error(request,'add address for delivery')
                    return redirect('checkout')
                payment = 'Cash on delivery'
                adress =  Address.objects.get(id = adress1)
                current_order = Order.objects.create(user = username, address = adress,total = total,payment_mode = payment)
                for i in cart_items:
                    obj = OrderProducts(order_id = current_order,user1 = username,product = i.product ,address1 = adress,quantity = i.quantity,amount = i.sub_total,status = 'ordered',size = i.size)
                    if obj.product.stock > 0: 
                        obj.product.stock = obj.product.stock - obj.quantity
                        obj.product.save()
                    else:
                        messages.error(request, 'out of stock')
                        return redirect('checkout')
                    obj.save()
                    i.delete()
            
                return redirect('confirm',current_order.id)
            
              
            return render(request, 'cart/checkout.html',context)
    
    return redirect('login')


def razor_pay(request):
    if 'users' in request.session:
            usm = request.session.get('users')
            username = Customuser.objects.get(email = usm)
            address = Address.objects.filter(user = username.id,is_available = True).order_by('id')
            cart_items = Cart.objects.filter(user_id = username.id).select_related('product__product_id')
            total = sum(i.sub_total for i in cart_items)
            cartcount = Cart.objects.filter(user_id = username).count()

            context = {
                'address':address,
                'cart_items':cart_items,
                'username' :username,
                'total':total,
                'cartcount':cartcount
            }
            wishcount = Wishlist.objects.filter(user_id = username).count()
            context['wishcount']=wishcount
            if request.method == 'POST':
                adress1 = request.POST.get('address',None)
                payment = 'Razorpay'
                adress =  Address.objects.get(id = adress1)
                current_order = Order.objects.create(user = username, address = adress,total = total,payment_mode = payment)
                for i in cart_items:
                    obj = OrderProducts(order_id = current_order,user1 = username,product = i.product ,address1 = adress,quantity = i.quantity,amount = i.sub_total,status = 'ordered',size = i.size)
                    if obj.product.stock > 0: 
                        obj.product.stock = obj.product.stock - obj.quantity
                        obj.product.save()
                    else:
                        messages.error(request, 'out of stock')
                        data = {'redirect_url':'/checkout/',
                                'error': True
                        }
                        return JsonResponse(data)
                    obj.save()
                    i.delete()
                data = {'redirect_url':'/confirm/',
                        'order_id1' : current_order.id ,
                        'completed': True 
                        }
                return JsonResponse(data) 
            


# not working make it work

def buy_now(request,id):
    if 'users' in request.session:
       
            usm = request.session.get('users')
            username = Customuser.objects.get(email = usm)
            address = Address.objects.filter(user = username.id)
            cartcount = Cart.objects.filter(user_id = username).count()
            produc = Product.objects.get(id = id)
            size = request.GET.get('size',None)
            quantity = request.GET.get('quantity',None)
            if size is not None and quantity is not None:
                total = int(produc.selling_price) * int(quantity) 
            try:
                buy_item =  ProductVariant.objects.get(product_id = id, size = size)
            except:
                buy_item = None
            context = {
                'address':address,
                'buy_item':buy_item,
                'username' :username,
                'total':total,
                'cartcount':cartcount,
                'size':size,
                'quantity': quantity
            }
            wishcount = Wishlist.objects.filter(user_id = username).count()
            context['wishcount']=wishcount
            if request.method == 'POST':
             if buy_item is not None:
                adress1 = request.POST.get('address',None)
    
                if not adress1:
                    messages.error(request,'add address for delivery')
                    return redirect('checkout')
                payment = request.POST['payment']
                adress =  Address.objects.get(id = adress1)
                current_order = Order.objects.create(user = username, address = adress,total = total,payment_mode = payment)
                obj = OrderProducts(order_id = current_order,user1 = username,product = buy_item ,address1 = adress,quantity = quantity,amount = total,status = 'ordered',size=size )
                if obj.product.stock >= 1: 
                    obj.product.stock = obj.product.stock - obj.quantity
                    obj.product.save()

                else:
                    messages.error(request, 'out of stock')
                    return redirect('checkout')
                obj.save()

                return redirect('confirm',current_order.id)
            

            return render(request, 'cart/checkout.html',context)
    return redirect('login')


def confirm(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        orders = Order.objects.get(id = id)
        order_items = OrderProducts.objects.filter(order_id = id)
        cartcount = Cart.objects.filter(user_id = username).count()
        context = {
            'username':username,
            'orders' : orders,
            'order_items': order_items,
            'cartcount':cartcount
        }
        wishcount = Wishlist.objects.filter(user_id = username).count()
        context['wishcount']=wishcount
        return render(request, 'cart/confirm.html',context)
    
    return redirect('login')


def wishlist(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        if username.is_blocked:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            return redirect('login') 
        cartcount = Cart.objects.filter(user_id = username).count() 
        wishlist_items = Wishlist.objects.filter(user_id = username).select_related('product_id__brand').order_by('-id')
        context = {
            'username': username,
            'cartcount':cartcount,
            'wishlist_items':wishlist_items,
            
        }
        wishcount = Wishlist.objects.filter(user_id = username).count()
        context['wishcount']=wishcount
        return render(request, 'cart/wishlist.html',context)
    return redirect('login')

def add_to_wish(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        products = Product.objects.get(id = id)
        if not Wishlist.objects.filter(product_id = products ,user_id = username):
            wish = Wishlist.objects.create(product_id = products,user_id = username)
            wish.stock = 'In Stock' if wish.product_id.quantity > 0 else 'Out of Stock'
            wish.save()
        nxt_url = request.GET.get('next','/')
        return redirect(nxt_url)
    messages.error(request,'you need to login')
    return redirect('login')

def remove_wish(request,id):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        prod = Product.objects.get(id = id)
        wish = Wishlist.objects.get(product_id = prod, user_id = username)
        wish.delete()
        nxt_url = request.GET.get('next','wishlist')
        return redirect(nxt_url)
    
    return redirect('login')