from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.


def view_coupon(request):
    if "users" in request.session:
        return redirect("page_not_found")
    if "admin" in request.session:
        coupons = Coupen.objects.all().order_by("-id")

        itm = request.GET.get("search",'')
        if itm.strip():
            coupons = coupons.filter(Q(title__icontains=itm.strip()) | Q(code__icontains=itm.strip()))
        else:
            page = request.GET.get("page", 1)
            paginator = Paginator(coupons, 10) 
            try:
                coupons = paginator.page(page)
            except PageNotAnInteger:
                coupons = paginator.page(1)
            except EmptyPage:
                coupons = paginator.page(paginator.num_pages)

        context = {"coupons": coupons}
        return render(request, "admin/admcoupons.html", context)
    
    return redirect("admlogin")


def add_coupon(request):
    if request.method == "POST":
        title = request.POST["title"]
        code = request.POST["code"]
        disamount = request.POST["disamount"]
        sdate = request.POST["sdate"]
        edate = request.POST["edate"]

        if title.strip() == '' or code.strip() == '':
            messages.error(request, "Enter valid title and code")
            return redirect("view_coupon")
        
        if float(disamount) <= 0:
            messages.error(request, "Enter a valid discount prize greater than 0 !! ")
            return redirect("view_coupon")
        
        if datetime.strptime(edate, '%Y-%m-%d') < datetime.strptime(sdate, '%Y-%m-%d'):
            messages.error(request, 'Enter valid dates!!')
            return redirect("view_coupon")
        
        if Coupen.objects.filter(code=code).exists():
            messages.error = (request, "entered  code already exists  try another")
            return redirect("view_coupon")

        Coupen.objects.create(
            title=title.strip(),
            code=code.strip(),
            valid_from=sdate,
            valid_to=edate,
            discount_amount=disamount,
        )
        messages.success(request, 'Coupon added successfully')
    return redirect("view_coupon")


def update_coupon(request, id):
    if request.method == "POST":
        title = request.POST["title"]
        code = request.POST["code"]
        sdate = request.POST["sdate"]
        edate = request.POST["edate"]
        disamount = request.POST["disamount"]
        try:
            coupon = Coupen.objects.get(id=id)
        except Coupen.DoesNotExist:
            coupon = None
        
        if title.strip() == '' or code.strip() == '':
            messages.error(request, "Enter valid title and code")
            return redirect("view_coupon")
        
        if float(disamount) <= 0:
            messages.error(request, "Enter a valid discount prize greater than 0 !! ")
            return redirect("view_coupon")
        
        if datetime.strptime(edate, '%Y-%m-%d') < datetime.strptime(sdate, '%Y-%m-%d'):
            messages.error(request, 'Enter valid dates!!')
            return redirect("view_coupon")
        
        if coupon is not None:
            coupon.title = title.strip()
            coupon.code = code.strip()
            coupon.valid_from = sdate
            coupon.valid_to = edate
            coupon.discount_amount = disamount
            coupon.save()
            messages.success(request, "Coupon updated Successfully ")
    return redirect("view_coupon")


def activation(request, id):
    if request.method == "POST":
        try:
            coupon = Coupen.objects.get(id=id)
        except Coupen.DoesNotExist:
            coupon = None
        if coupon is not None:
            if coupon.is_active == True:
                coupon.is_active = False
                coupon.save()
                messages.success(request, "Coupon Deactivated Successfully")
            else:
                coupon.is_active = True
                coupon.save()
                messages.success(request, "Coupon Activated Successfully ")

    return redirect("view_coupon")


def view_brand_offers(request):
    if "users" in request.session:
        return redirect("page_not_found")
    if "admin" in request.session:
        boffers = BrandOffer.objects.all().order_by("-id")
        brand = Brand.objects.all()
        itm = request.GET.get("search",'')
        if itm.strip():
            boffers =  boffers.filter(brand__brand_name__icontains = itm.strip())
        else:
            page = request.GET.get("page", 1)
            paginator = Paginator(boffers, 10) 
            try:
                boffers = paginator.page(page)
            except PageNotAnInteger:
                boffers = paginator.page(1)
            except EmptyPage:
                boffers = paginator.page(paginator.num_pages)
                
        context = {"offers": boffers, "brands": brand}
        return render(request, "admin/brand_offers.html", context)

    return redirect("admlogin")


def add_brand_offer(request):
    if request.method == "POST":
        new_brand = request.POST["brand"]
        perc = request.POST["perc"]
        try:
            brand = Brand.objects.get(id=new_brand)
        except:
            brand = None
        if brand is not None:
            if BrandOffer.objects.filter(brand=brand).exists():
                messages.error(request, "Already Offer for this Brand")
                return redirect("view_brand_offers")
            if float(perc) <= 0:
                messages.error(request, "Invalid Offer Amount")
                return redirect("view_brand_offers")
            BrandOffer.objects.create(brand=brand, offer_percentage=perc)
            messages.success(request, "Offer Created Successfully")
            
    return redirect("view_brand_offers")


def update_brand_offer(request, id):
    if request.method == "POST":
        try:
            boffer = BrandOffer.objects.get(id=id)
        except:
            boffer = None
        if boffer is not None:
            perc = request.POST["perc"]
            
            if float(perc) <= 0:
                messages.error(request, "Invalid Offer Amount ")
                return redirect("view_brand_offers")
            
            boffer.offer_percentage = perc
           
            boffer.save()
            messages.success(request, "Offer Updated Successfully") 
            
    return redirect("view_brand_offers")


def active_brand_offer(request, id):
    if request.method == "POST":
        try:
            boffer = BrandOffer.objects.get(id=id)
        except:
            boffer = None
        if boffer is not None:
            if boffer.is_active:
                boffer.is_active = False
                messages.success(request, "Offer Deactivated Successfully")
            else:
                boffer.is_active = True
                messages.success(request, "Offer Activated Successfully")
                
            boffer.save()

    return redirect("view_brand_offers")


def view_product_offers(request):
    if "users" in request.session:
        return redirect("page_not_found")
    if "admin" in request.session:
        poffers = ProductOffer.objects.all().order_by("-id")
        product = Product.objects.all()
        itm = request.GET.get("search",'')
        if itm.strip():
            poffers =  poffers.filter(Q(product__name__icontains = itm.strip()) |
                                      Q(product__brand__brand_name__icontains = itm.strip()) )
        else:
            page = request.GET.get("page", 1)
            paginator = Paginator(poffers, 10) 
            try:
                poffers = paginator.page(page)
            except PageNotAnInteger:
                poffers = paginator.page(1)
            except EmptyPage:
                poffers = paginator.page(paginator.num_pages)
                
        context = {"offers": poffers, "products": product}
        return render(request, "admin/product_offers.html", context)

    return redirect("admlogin")


def add_product_offer(request):
    if request.method == "POST":
        new_prod = request.POST["product"]
        perc = request.POST["perc"]
        try:
            product = Product.objects.get(id=new_prod)
        except:
            product = None
        if product is not None:
            if ProductOffer.objects.filter(product=product).exists():
                messages.error(request, "Already Offer for this Product")
                return redirect("view_product_offers")
            if float(perc) <= 0:
                messages.error(request, "Invalid Offer")
                return redirect("view_product_offers")
            ProductOffer.objects.create(product=product, offer_percentage=perc)
            messages.success(request , "Offer Created Successfully")
    return redirect("view_product_offers")


def update_product_offer(request, id):
    if request.method == "POST":
        try:
            poffer = ProductOffer.objects.get(id=id)
        except:
            poffer = None
        if poffer is not None:
            perc = request.POST["perc"]
            
            if float(perc) <= 0:
                messages.error(request, "Invalid Offer Amount ")
                return redirect("view_product_offers")
            
            poffer.offer_percentage = perc
            poffer.save()
            messages.success(request, "Offer Updated Successfully") 
            
    return redirect("view_product_offers")


def active_product_offer(request, id):
    if request.method == "POST":
        try:
            poffer = ProductOffer.objects.get(id=id)
        except:
            poffer = None
        if poffer is not None:
            if poffer.is_active:
                poffer.is_active = False
                messages.success(request, "Offer Deactivated Successfully")
            else:
                poffer.is_active = True
                messages.success(request, "Offer Activated Successfully")

            poffer.save()

    return redirect("view_product_offers")
