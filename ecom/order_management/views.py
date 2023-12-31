from django.shortcuts import render,redirect
from .models import *
from datetime import datetime
# Create your views here.

def admorders(request):
    if 'admin' in request.session:
        orders = OrderProducts.objects.all().order_by('-id')
        context = {
            'order_items':orders
        }
        return render(request,'admin/admorders.html',context )

    return redirect('admlogin')


def update_status(request,id):
    if request.method == 'POST': 
        status1 = request.POST['status']
        orders = OrderProducts.objects.get(id = id)
        orders.status = status1
        orders.save()
    return redirect('admorders')


def update_date(request,id):
    if request.method == 'POST':
        new_date1 = request.POST['date']
        new_date = datetime.strptime(new_date1, '%Y-%m-%d').date()
        orders = OrderProducts.objects.get(id = id)
        orders.delivery_date = new_date
        print(new_date1,new_date)
        orders.save()
        
    return redirect('admorders')