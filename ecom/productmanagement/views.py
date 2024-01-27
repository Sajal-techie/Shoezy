from django.shortcuts import render, redirect
from .models import *
from categorymanagement.models import Brand
import os
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
import re


# view products
def view_products(request):
    if "users" in request.session:
        return redirect("page_not_found")
    try:
        if "admin" in request.session:
            products = Product.objects.all().order_by("-id")
            productvariant = ProductVariant.objects.all()
            brands = Brand.objects.all()
            itm = request.GET.get("search", "")
            if itm.strip():
                products = products.filter(Q(name__icontains = itm.strip()) |
                                        Q(brand__brand_name__icontains = itm.strip()))
            else:
            # paginator
                page = request.GET.get("page", 1)
                paginator = Paginator(products, 10)
                try:
                    products = paginator.page(page)
                except PageNotAnInteger:
                    products = paginator.page(1)
                except EmptyPage:
                    products = paginator.page(paginator.num_pages)
                
            mulimage = ProductImages.objects.all()
            context = {
                "product": products,
                "brands": brands,
                "imagess": mulimage,
                "productvariant": productvariant,
            }
            return render(request, "admin/admproducts.html", context)
    except Exception as e:
        print(e)
        
    return redirect("admlogin")


def add_product(request):
    try:
        if request.method == "POST":
            name = request.POST.get("name", "")
            category = request.POST["category"]
            brand_id = request.POST["brand"]
            noofferprice = request.POST["noofferprice"]
            offerprice = request.POST["offerprice"]
            desc = request.POST["desc"]

            if "croppedImageData" in request.POST:
                cropped_image = request.POST.get("croppedImageData", None)

                if cropped_image:
                    format, imgstr = cropped_image.split(";base64,")
                    ext = re.search(r"/(.*?)$", format).group(1)

                    # Convert base64 string to a Django ContentFile
                    decoded_file = base64.b64decode(imgstr)
                    img_name = ContentFile(decoded_file, name=f"cropped_image.{ext}")
            else:
                img_name = (
                    request.FILES.get("image1") if "image1" in request.FILES else None
                )
            if not name.strip():
                messages.error(request, " Enter a valid product name ")
                return redirect("view_products")
            
            if int(noofferprice) < int(offerprice):
                messages.error(request, "Offer price must be less than no offer price")
                return redirect("view_products")

            if int(noofferprice) <= 0 or int(offerprice) <= 0:
                messages.error(request, "Enter a valid price (greater than 0)")
                return redirect("view_products")

            brand = Brand.objects.get(id=brand_id)
            pro = Product(
                name=name.strip(),
                category=category,
                brand=brand,
                original_price=noofferprice,
                selling_price=offerprice,
                description=desc.strip(),
            )

            # add image to product table
            if img_name:
                pro.image1 = img_name
            pro.save()

            # add images to productimages table
            for i in range(2, 5):
                image_name = f"image{i}"
                image = request.FILES.get(image_name)
                if image:
                    ProductImages.objects.create(product=pro, images=image, image_number=i)
            messages.success(request, F"Product- {name}  added successfully")
            return redirect("view_products")
    except Exception as e:
        print(e)
    return redirect("view_products")


def add_variant(request, id): 
    try:
        if request.method == "POST":
            color = request.POST["color"]
            size = request.POST["size"]
            quantity = request.POST["quantity"]

            product = Product.objects.get(id=id)

            if ProductVariant.objects.filter(
                product_id=product, size=size
            ).exists():
                messages.error(request, F"{product.name} of size ({size})  already Exists ")
                return redirect("view_products")

            if int(quantity) <= 0:
                messages.error(request, "Enter a valid Quantity (greater than 0)")
                return redirect("view_products")

            ProductVariant.objects.create(
                product_id=product, size=size, stock=quantity, color=color
            )
            messages.success(request, F"Variant of {product.name} Created successfully ")
    except Exception as e:
        print(e)
    return redirect("view_products")


def edit_variant(request, id):
    try:
        if request.method == "POST":
            quantity = request.POST["quantity"]
            if int(quantity) <= 0:
                messages.error(request, "Enter a valid Quantity (greater than 0)")
                return redirect("view_products")

            variant = ProductVariant.objects.get(id=id)
            variant.stock = quantity
            variant.save()
            messages.success(request, F"{variant.product_id.name} of size {variant.size} updated successfully  ")
        return redirect("view_products")
    except Exception as e:
        print(e)
        
    return redirect("view_products")
    


def delete_variant(request, id):
    variant = ProductVariant.objects.get(id=id)
    variant.delete()
    messages.success(request, F"{variant.product_id.name} of size{variant.size} deleted ")
    return redirect("view_products")


def edit_product(request, id):
    try:
        exist = Product.objects.get(id=id)
        old_image = ProductImages.objects.filter(product_id=id)

        if request.method == "POST":
            name = request.POST["name"]
            category = request.POST["category"]
            brand = request.POST["brand"]
            noofferprice = request.POST["noofferprice"]
            offerprice = request.POST["offerprice"]
            desc = request.POST["desc"]
            img_name = request.FILES.get("image1", None)

            if not name.strip():
                messages.error(request, " Enter a valid product name ")
                return redirect("view_products")
            
            if float(noofferprice) <= 0 or float(offerprice) <= 0:
                messages.error(request, "Enter a valid price (greater than 0)")
                return redirect("view_products")

            exist.name = name
            exist.category = category
            exist.brand = Brand.objects.get(id=brand)
            exist.original_price = noofferprice
            exist.selling_price = offerprice
            exist.description = desc

            # deleting excisting image and uploading new images 
            if img_name is not None:
                if exist.image1:
                    os.remove(exist.image1.path)
                exist.image1 = img_name
            exist.save()
            messages.success(request, F"{exist.name} Updated Successfully ")
            
            for i in range(2, 5):
                image_name = f"image{i}"
                image = request.FILES.get(image_name, None)

                if image:
                    # Delete old images
                    for j in old_image:
                        k = os.remove(j.images.path) if j.image_number == i else None
                        old_image.filter(image_number=i).delete()
                    # Add new images
                    ProductImages.objects.create(
                        product=exist, images=image, image_number=i
                    )
            return redirect("view_products")
        
    except Exception as e:
        print(e)
        
    return redirect("view_products")


def delete_product(request, id):
    deletepro = Product.objects.get(id=id)
    deletepro.delete()
    return redirect("view_products")


def list_product(request, id):
    try:
        listproduct = Product.objects.get(id=id)
    except Exception :
        listproduct = None
    if listproduct is not None:
        if listproduct.is_listed:
            listproduct.is_listed = False
            messages.success(request, F"{listproduct.name} is unlisted ")
        else:
            listproduct.is_listed = True
            messages.success(request, F"{listproduct.name} is listed ")

        listproduct.save()
    
    return redirect("view_products")
