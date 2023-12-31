from django.shortcuts import render,redirect
from .models import *
from datetime import datetime
# Create your views here.

def admorders(request):
    if 'users' in request.session:
        return redirect('page_not_found')
    if 'admin' in request.session:
        orders = OrderProducts.objects.all().order_by('-id')
        for order in orders:
            if order.delivery_date < datetime.now().date():
                order.status = 'delivered'
            if order.delivery_date == datetime.now().date() and (order.status == 'ordered' or order.status == 'shipped'):
                order.status = 'out for delivery'
                order.save()
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
        if status1 == 'delivered' or status1 =='out for delivery':
            orders.delivery_date = datetime.now().date() 
        orders.save()
    return redirect('admorders')


def update_date(request,id):
    if request.method == 'POST':
        new_date1 = request.POST['date']
        new_date = datetime.strptime(new_date1, '%Y-%m-%d').date()
        orders = OrderProducts.objects.get(id = id)
        orders.delivery_date = new_date
        orders.save()
        
    return redirect('admorders')