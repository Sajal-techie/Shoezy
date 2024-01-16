from django.shortcuts import render,redirect
from . models import Brand
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
def viewbrand(request):
    if 'users' in request.session:
        return redirect('page_not_found')
    if 'admin' in request.session:
        brands = Brand.objects.all().order_by('id')
        
        brandname = request.GET.get('name')
        if brandname:
            brands = brands.filter(brand_name__icontains = brandname )
            
        page = request.GET.get('page',1)
        paginator = Paginator(brands,10)  
        try:
            brands =  paginator.page(page)
        except PageNotAnInteger:
            brands =  paginator.page(1)
        except EmptyPage:
            brands =  paginator.page(paginator.num_pages)
            
        context = {
            'brand': brands
        }
        return render(request,'admin/admcategory.html',context)
    return redirect('admlogin')


def add_brand(request):
    if request.method == 'POST':
        bname = request.POST['name']
        brand = Brand(brand_name = bname)
        brand.save()
        return redirect('viewbrand')
    return redirect('viewbrand')


def edit_brand(request,id):
    if request.method == 'POST':
        bname = request.POST['name']
        brand = Brand.objects.get(id = id)
        brand.brand_name = bname
        brand.save()
        return redirect('viewbrand')
    return redirect('viewbrand')


def list_brand(request,id):
        brand = Brand.objects.get(id = id)
        if brand.is_listed == True:
            brand.is_listed = False 
            brand.save()
            return redirect('viewbrand')
        else: 
            brand.is_listed = True 
            brand.save()
            return redirect('viewbrand')

def delete_brand(request,id):
    brand = Brand.objects.get(id = id)
    brand.delete()
    return redirect('viewbrand')

