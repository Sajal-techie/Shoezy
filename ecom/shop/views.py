from django.shortcuts import render
from home.models import Customuser
# Create your views here.

def shop(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        return render(request, 'shop/shop.html', {'username':username.first_name})
    return render(request, 'shop/shop.html')

def singleproduct(request):
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        return render(request, 'shop/singleproduct.html',{'username':username.first_name})

    return render(request, 'shop/singleproduct.html')
