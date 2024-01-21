from django.shortcuts import render,redirect
from home.models import Customuser
from django.views.decorators.cache import never_cache
from productmanagement.models import *
from django.contrib import messages
from categorymanagement.models import Brand
from cart.views import check_cart,check_wishlist
from cart.models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def shop(request): 
    try:
        context = {}
        try:
            products = Product.objects.filter(is_listed = True, brand_id__is_listed = True).order_by('-id')
        except Product.DoesNotExist:
            products = None
        # for i in products:
        #     offer = i.offer_price()
        #     print(offer,i.name)
        try:
            brands = Brand.objects.filter(is_listed = True).order_by('id')
        except Product.DoesNotExist:
            brands = None
        
        #paginator
        page = request.GET.get('page',1)  
          
        # list all available color and size 
        try:
            color_list =  ProductVariant.objects.values('color').distinct()
        except ProductVariant.DoesNotExist:
            color_list = None 
            
        try:
            size_list = ProductVariant.objects.values('size').distinct()
        except ProductVariant.DoesNotExist:
            size_list = None
                
        #  filtering products  
        try: 

                men = request.GET.get('men')  
                women = request.GET.get('women')
                brand_names = request.GET.getlist('brandname')
                color_names = request.GET.getlist('colors')
                sizes = request.GET.getlist('size') 
                discount = request.GET.get('dis') 
                lowest = request.GET.get('lowest')
                highest = request.GET.get('highest')
                sortby = request.GET.get('sort_by') 
                itm = request.GET.get('search_items') 
                
                if itm:
                    products = products.filter(Q( Q(name__icontains = itm) | Q(brand__brand_name__icontains = itm) )) 
                context['srcitem'] = itm
                             
                if men and women:
                    products = products.filter( Q(category = men) | Q(category = women) | Q(category = 'all')).order_by('-id')   
                elif women:
                    products = products.filter( category = women).order_by('-id') 
                elif men:
                    products = products.filter( category = men).order_by('-id') 
                context['men'] = men
                context['women'] = women
                
                if brand_names:
                    products = products.filter(brand_id__brand_name__in = brand_names).order_by('-id') 
                context['brand_names'] = brand_names

                if color_names:
                    products = products.filter(productvariant__color__in = color_names).distinct()
                context['color_names'] = color_names
                    
                if sizes:
                    products = products.filter(productvariant__size__in = sizes).distinct()
                context['sizes']= sizes
                    
                if discount:
                    products = products.filter(discount_percentage__gte = discount)
                context['discount'] = discount
                    
                if lowest and highest:
                    if int(lowest) > int(highest):
                        messages.error(request,'Starting prize must be less than Highest prize')
                        
                    products = products.filter(selling_price__range = (lowest,highest))
                elif lowest:
                    products = products.filter(selling_price__gte = lowest)
                elif highest:
                    products = products.filter(selling_price__lte = highest)  
                    
                context['lowest'] = lowest
                context['highest'] = highest
                    
                if sortby:
                    if sortby == 'price_high':
                        products = products.order_by('-selling_price') 
                    elif sortby == 'price_low':
                        products = products.order_by('selling_price')   
                        
                context['sort_by'] = sortby
            

                paginator = Paginator(products,9) 
                try: 
                    products = paginator.page(page)
                except PageNotAnInteger:
                    products.page(1)
                except EmptyPage:
                    products = paginator.page(paginator.num_pages)
                    
                context['product'] = products
                context['brand'] = brands
                context['color_list'] = color_list      
                context['size_list'] = size_list
             
        except Exception as e:
            print(e)
        
        if 'users' in request.session:
            
            usm = request.session.get('users')
            try:
                username = Customuser.objects.get(email = usm)
            except Customuser.DoesNotExist:
                username = None
            
            context['username'] = username
            cart_item = Cart.objects.filter(user_id = username).values('product_id')
            cartcount = Cart.objects.filter(user_id = username).count()
            context['cart_item'] = cart_item
            context['cartcount'] = cartcount
            wishcount = Wishlist.objects.filter(user_id = username).count()
            context['wishcount']=wishcount
            
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
            
    except Exception as e:
        print(e)

    return render(request, 'shop/shop.html',context)


def singleproduct(request,id):
    try:
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
            # is_in_cart = check_cart(username,id)          
            # context['is_in_cart']= is_in_cart             
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
            
    except Exception as e:
        print(e)
        
    return render(request, 'shop/singleproduct.html',context)


# resetting filters
def reset_filters(request):
    return redirect('shop')