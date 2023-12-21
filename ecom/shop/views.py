from django.shortcuts import render
from home.models import Customuser
from django.views.decorators.cache import never_cache
from productmanagement.models import Product,ProductImages
from categorymanagement.models import Brand
# Create your views here.

def shop(request):
    products = Product.objects.filter(is_listed = True, brand_id__is_listed = True)
    brands = Brand.objects.filter(is_listed = True)
    # multiple = ProductImages.objects.all()
    context = {
        'product' : products,
        'brand' : brands
    }
    if 'users' in request.session:
        
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        return render(request, 'shop/shop.html', {'username':username.first_name,
                                                  'product' : products,
                                                  'brand' : brands})
    return render(request, 'shop/shop.html',context)

def singleproduct(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        return render(request, 'shop/singleproduct.html',{'username':username.first_name})

    return render(request, 'shop/singleproduct.html')
