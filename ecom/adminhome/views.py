from django.shortcuts import render

# Create your views here.

def admlogin(request):
    return render(request, 'admin/admlogin.html')


def admhome(request):
    return render(request,'admin/admhome.html')


def admusers(request):
    return render(request,'admin/admusers.html')

def admproducts(request):
    return render(request,'admin/admproducts.html')

def admcategories(request):
    return render(request,'admin/admcategory.html')

def admorders(request):
    return render(request,'admin/admorders.html')

def admreturns(request):
    return render(request,'admin/admreturns.html')

def admcoupons(request):
    return render(request,'admin/admcoupons.html')

def admbanners(request):
    return render(request,'admin/admbanners.html')
