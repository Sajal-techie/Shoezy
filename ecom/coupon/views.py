from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def view_coupon(request):
    # if 'users' in request.session:
    #     return redirect('page_not_found')
    if 'admin' in request.session:
        coupons = Coupen.objects.all().order_by('-id')
        
        itm = request.GET.get('search')
        if itm:
            coupons = coupons.filter(Q(title__icontains = itm) | Q(code__icontains = itm))
            
        context = {
            'coupons':coupons
        }
    return render(request,'admin/admcoupons.html',context)


def add_coupon(request):
    if request.method == 'POST':
        title = request.POST['title']
        code = request.POST['code']
        disamount = request.POST['disamount']
        sdate = request.POST['sdate']
        edate = request.POST['edate']
        
        if Coupen.objects.filter(code = code).exists():
            messages.error = (request,'entered  code already exists  try another')
            print('hi')
            return redirect('view_coupon')
        
        Coupen.objects.create(title = title,
                              code = code,
                              valid_from = sdate,
                              valid_to = edate,
                              discount_amount = disamount)
        
    return redirect('view_coupon') 


def update_coupon(request, id):
    if request.method == 'POST':
        title = request.POST['title']
        code = request.POST['code']
        sdate = request.POST['sdate']
        edate = request.POST['edate']
        disamount = request.POST['disamount']
        try:
            coupon = Coupen.objects.get(id = id)
        except Coupen.DoesNotExist:
            coupon = None
        if coupon is not None:
            coupon.title = title
            coupon.code =code
            coupon.valid_from = sdate
            coupon.valid_to = edate
            coupon.discount_amount = disamount
            coupon.save()
            
    return redirect('view_coupon')


def activation(request,id):
    if request.method == 'POST':
        try:
            coupon = Coupen.objects.get(id = id)
        except Coupen.DoesNotExist:
            coupon = None
        if coupon is not None:
            if coupon.is_active == True:
                coupon.is_active = False
                coupon.save()
            else:
                coupon.is_active = True
                coupon.save()
            
    return redirect('view_coupon')