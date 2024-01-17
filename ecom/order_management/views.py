from django.shortcuts import render,redirect
from .models import *
from datetime import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.contrib import messages


def admorders(request):
    if 'users' in request.session:
        return redirect('page_not_found')
    if 'admin' in request.session:
        orders = OrderProducts.objects.all().order_by('-id')

        search = request.GET.get('search','')
        if search:
            orders = orders.filter(Q( id__contains = search) | Q(status__icontains = search ))
            
        # paginator
        page = request.GET.get('page',1)
        paginator = Paginator(orders,10)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
            
            
        context = { 
            'order_items':orders,
            'search':search
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
        
        if new_date < orders.order_id.order_date:
            messages.error(request, 'Delivery date must be after order date')
            return redirect('admorders')
        
        orders.delivery_date = new_date
        orders.save()
        
    return redirect('admorders')