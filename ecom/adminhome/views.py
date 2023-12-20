from django.shortcuts import render,redirect
from home.models import Customuser
from django.db.models import Q
# Create your views here.

def admlogin(request):
    return render(request, 'admin/admlogin.html')


def admhome(request):
    return render(request,'admin/admhome.html')


def admusers(request):
    user_list = Customuser.objects.all().order_by('id')
    context = {
        'user_details': user_list
    }
    return render(request,'admin/admusers.html',context)

def block_user(request,id):
    block = Customuser.objects.get(id = id)
    if not block.is_blocked:
        block.is_blocked = True
        block.save()
        return redirect('admusers') 
    return redirect('admusers')

def unblock_user(request,id):
    unblock = Customuser.objects.get(id = id)
    if unblock.is_blocked:
        unblock.is_blocked = False
        unblock.save()
        return redirect('admusers') 
    return redirect('admusers')


def user_search(request):
    sname = request.GET['searchuser']
    user_list = Customuser.objects.filter(Q(first_name__icontains = sname ) | Q(email__icontains = sname) ).order_by('id')
    context = {
        'user_details': user_list
    }
    return render(request,'admin/admusers.html',context)

def admbanners(request):
    return render(request,'admin/admbanners.html')
