from django.shortcuts import render,redirect
from .models import Product,ProductImages
from categorymanagement. models import Brand
import os

# view products
def view_products(request):
    if 'users' in request.session:
        return redirect('page_not_found')
    if 'admin' in request.session:
        products = Product.objects.all().order_by('-id')
        brands = Brand.objects.all()

        mulimage = ProductImages.objects.all()
        context = {
            'product':products,
            'brands': brands,
            'imagess':mulimage
            
        }
        return render(request,'admin/admproducts.html',context)
    return redirect('admlogin')

def add_product(request):
    
        if request.method == 'POST':
            name = request.POST['name']
            category = request.POST['category']
            brand_id = request.POST['brand']
            noofferprice = request.POST['noofferprice']
            offerprice = request.POST['offerprice']
            desc = request.POST['desc']
            quantity = request.POST['quantity']
            img_name = request.FILES.get('image1') if 'image1' in request.FILES else None
            brand = Brand.objects.get(id = brand_id)
            pro = Product(name = name,
                        category = category,
                        brand = brand,
                        original_price = noofferprice,
                        selling_price = offerprice,
                        description = desc,
                        quantity = quantity,)
            
            # add image to product table
            if img_name:
                pro.image1 = img_name
            pro.save()
            
            # add images to productimages table
            for i in range(2,5):
                image_name = f"image{i}"
                image = request.FILES.get(image_name)            
                if image:               
                    ProductImages.objects.create(product = pro , images = image, image_number = i) 
                                
            return redirect('view_products')
        
        return redirect('view_products')
    
    


def edit_product(request,id):
    exist = Product.objects.get(id = id)
    old_image = ProductImages.objects.filter(product_id = id)
    
    if request.method == "POST":
        name = request.POST['name']
        category = request.POST['category']
        brand = request.POST['brand']
        noofferprice = request.POST['noofferprice']
        offerprice = request.POST['offerprice']
        desc = request.POST['desc']
        quantity = request.POST['quantity']
        
        img_name = request.FILES.get('image1',None) 
        
        exist.name = name
        exist.category = category
        exist.brand = Brand.objects.get(id = brand )
        exist.original_price = noofferprice
        exist.selling_price = offerprice
        exist.description = desc
        exist.quantity = quantity
        
        
        if img_name is not None :
            if exist.image1:
                os.remove(exist.image1.path)
            exist.image1 = img_name
        exist.save()
        
        
        for i in range(2, 5):
            image_name = f"image{i}"
            image = request.FILES.get(image_name, None)

            if image:
                # Delete old images
                for j in old_image:
                    k = os.remove(j.images.path) if j.image_number == i else None 
                    old_image.filter(image_number = i).delete()
                # Add new images
                ProductImages.objects.create(product=exist, images=image, image_number = i)
                         
        return redirect('view_products')
    return redirect('view_products')


def delete_product(request,id):
    deletepro = Product.objects.get(id = id)
    deletepro.delete()
    return redirect('view_products')
    
    
def list_product(request,id):
    listproduct = Product.objects.get(id = id)
    
    if listproduct.is_listed:
        listproduct.is_listed = False
    else:
        listproduct.is_listed = True
            
    listproduct.save()
    return redirect('view_products')

def search_product(request):
    search = request.GET['search']
    items   = Product.objects.filter(name__icontains = search)
    context = {
        'product': items
    }
    return render(request, 'admin/admproducts.html',context)