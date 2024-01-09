from django.shortcuts import render,redirect
from home.models import Customuser
from django.views.decorators.cache import never_cache
from productmanagement.models import *
from django.contrib import messages
from categorymanagement.models import Brand
from cart.views import check_cart,check_wishlist
from cart.models import *
# Create your views here.

def shop(request):
    
    categor = request.GET.get('category')
    brand_names = request.GET.get('brand')
    
    products = Product.objects.filter(is_listed = True, brand_id__is_listed = True).order_by('-id')
    brands = Brand.objects.filter(is_listed = True).order_by('id')
    # multiple = ProductImages.objects.all()

    if categor:
        products = Product.objects.filter(is_listed = True, brand_id__is_listed = True,category = categor).order_by('-id') 

    if brand_names:
        products = Product.objects.filter(is_listed = True, brand_id__is_listed = True,brand_id__brand_name = brand_names).order_by('-id') 
        
    

    
    
    
    context = {
        'product' : products,
        'brand' : brands,
        
    }
    
    if 'users' in request.session:
        
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        context['username'] = username
        cart_item = Cart.objects.filter(user_id = username).values('product_id')
        cartcount = Cart.objects.filter(user_id = username).count()
        context['cart_item'] = cart_item
        context['cartcount'] = cartcount
        wishcount = Wishlist.objects.filter(user_id = username).count()
        context['wishcount']=wishcount
        
        # cartlist = []
        # cart_items = Cart.objects.filter(user_id = username)
        # for i in cart_items:
        #     cartlist.append(i.product.product_id.id)
        # context['cartlist'] = cartlist 
        wishlist1 = []
        wishitems = Wishlist.objects.filter(user_id = username)
        for j in wishitems:
            wishlist1.append(j.product_id.id)
        context['wishlist1'] = wishlist1
        if not username.is_blocked:      
            return render(request, 'shop/shop.html', context)
        else:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            return redirect('login')
        
    return render(request, 'shop/shop.html',context)


def singleproduct(request,id):
    products = Product.objects.filter(id = id)
    brands = Brand.objects.filter(id = id)
    multiple = ProductImages.objects.filter(product_id = id )
    productvariant = ProductVariant.objects.filter(product_id = id)[:1]
    productvariants = ProductVariant.objects.filter(product_id = id)
    
    context = {
        'product' : products,
        'brand' : brands,
        'multi_image' : multiple,
        'productvariant':productvariant,
        'productvariants':productvariants,
    }
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        if username.is_blocked:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            return redirect('login') 
        # is_in_cart = check_cart(username,id)          # dubt area
        # context['is_in_cart']= is_in_cart             # doubt area
        is_in_wish = check_wishlist(username,id)      
        context['is_in_wish']= is_in_wish            
        context['username'] = username
        cartcount = Cart.objects.filter(user_id = username).count()
        context['cartcount']=cartcount
        wishcount = Wishlist.objects.filter(user_id = username).count()
        context['wishcount']=wishcount
        
        if not username.is_blocked:     
             
            return render(request, 'shop/singleproduct.html', context)
        else:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            
            return redirect('login')
        
    return render(request, 'shop/singleproduct.html',context)



def seachitems(request):
    itm = request.GET['search_items']
    products = Product.objects.filter(is_listed = True, brand_id__is_listed = True,name__icontains = itm)
    brands = Brand.objects.filter(is_listed = True)
    context = {
        'product' : products,
        'brand' : brands
    }
    

    if 'users' in request.session:
        
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        context['username'] = username
        
        if not username.is_blocked:      
            return render(request, 'shop/shop.html', context)
        else:
            if 'users' in request.session:
                del request.session['users']
            messages.error(request,'you are blocked ')
            return redirect('login')
        
    return render(request, 'shop/shop.html',context)
