from django.shortcuts import render,redirect
from django.contrib import messages
from home.models import Customuser
from productmanagement.models import Product,ProductImages
from . models import Cart

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
        
    return render(request, 'cart/cart.html',context)





def addto_cart(request,p_id):
    if 'users' in request.session:
        context={}
        usm = request.session.get('users')
        user2 = Customuser.objects.get(email = usm)
        product = Product.objects.get(id = p_id)
        cart_item = Cart.objects.get(user_id = user2,product_id= product)
        if cart_item is None:
            if product.quantity > 0:
                Cart.objects.create( user_id = user2 ,product_id = product,quantity = 1)
                is_in_cart = check_cart(user2,product.id)
                context={
                    'is_in_cart':is_in_cart
                }
                
        next_url = request.GET.get('next', '/')
        return redirect(next_url,context)
        
        
        
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