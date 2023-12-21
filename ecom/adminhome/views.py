from django.shortcuts import render,redirect
from home.models import Customuser
from django.db.models import Q
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages


@never_cache
def admlogin(request):
    if 'admin' in request.session:
        return redirect('admhome')
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        
        user = authenticate(username = name,password = password)
        if user is not None:
            request.session['admin'] = name
            return redirect('admhome')
        else:
            messages.error(request,'invalid username or password')
            return redirect('admlogin')
    
    return render(request, 'admin/admlogin.html')


@never_cache
def admhome(request):
    if 'admin' in request.session:
        return render(request,'admin/admhome.html' )
    return render(request,'admin/admlogin.html')


def admusers(request):
    if 'admin' in request.session:
        user_list = Customuser.objects.all().order_by('id')
        context = {
            'user_details': user_list
        }
        return render(request,'admin/admusers.html',context)
    return redirect('admlogin')

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


def admlogout(request):
    if 'admin' in request.session:
        del request.session['admin']
    return redirect('admlogin')