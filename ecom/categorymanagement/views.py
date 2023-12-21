from django.shortcuts import render,redirect
from . models import Brand
# Create your views here.
def viewbrand(request):
    if 'admin' in request.session:
        brands = Brand.objects.all().order_by('id')
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

def search_brand(request):
    brandname = request.GET['name']
    brands = Brand.objects.filter(brand_name__icontains = brandname )
    context = {
        'brand': brands
    }
    return render(request,'admin/admcategory.html',context)