from django.shortcuts import render

# Create your views here.

def shop(request):
    return render(request, 'shop/shop.html')

def singleproduct(request):
    return render(request, 'shop/singleproduct.html')
