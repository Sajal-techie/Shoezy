from django.shortcuts import render, redirect
from .models import Brand
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Create your views here.
def viewbrand(request):
    if "users" in request.session:
        return redirect("page_not_found")
    try:
        if "admin" in request.session:
            brands = Brand.objects.all().order_by("id")

            # search
            brandname = request.GET.get("name", "")
            if brandname.strip():
                brands = brands.filter(brand_name__icontains=brandname.strip())
            else:
                # paginator
                page = request.GET.get("page", 1)
                paginator = Paginator(brands, 10)
                try:
                    brands = paginator.page(page)
                except PageNotAnInteger:
                    brands = paginator.page(1)
                except EmptyPage:
                    brands = paginator.page(paginator.num_pages)

            context = {"brand": brands}
            return render(request, "admin/admcategory.html", context)
        
    except Exception as e:
        print(e)
        
    return redirect("admlogin")


def add_brand(request):
    try:
        if request.method == "POST":
            bname = request.POST["name"]
            if not bname.strip():
                messages.error(request, "Enter a valid brand name")
                return redirect("viewbrand")
            brand = Brand(brand_name=bname)
            brand.save()
            messages.success(request, F"{bname} added Successfully")
            return redirect("viewbrand")
        
    except Exception as e:
        print(e)
        
    return redirect("viewbrand")


def edit_brand(request, id):
    try:
        if request.method == "POST":
            bname = request.POST["name"]
            if not bname.strip():
                messages.error(request, "Enter a valid brand name")
                return redirect("viewbrand")
            brand = Brand.objects.get(id=id)
            brand.brand_name = bname.strip()
            brand.save()
            messages.success(request, F"{bname} Updated successfully ")
            return redirect("viewbrand")
        
    except Exception as e:
        print(e)
        
    return redirect("viewbrand")


def list_brand(request, id):
    try:
        brand = Brand.objects.get(id=id)
        if brand.is_listed == True:
            brand.is_listed = False
            brand.save()
            messages.success(request, F"{brand.brand_name} is unlisted ")
            return redirect("viewbrand")
        else:
            brand.is_listed = True
            brand.save()
            messages.success(request, F"{brand.brand_name} is listed ")
            return redirect("viewbrand")
    except Exception as e:
        print(e)
    return redirect("viewbrand")
