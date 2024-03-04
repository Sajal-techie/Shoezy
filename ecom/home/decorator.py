from django.shortcuts import render, redirect
from .models import Customuser
from django.contrib import messages

def session_handler(view_func):
    def wrapper_func(request, *args, **kwargs):
        user_email = request.session.get('users',None)
        try:
            username = Customuser.objects.get(email = user_email)
            if username.is_blocked:
                del request.session["users"]
                messages.error(request, "You are blocked")
                return redirect("login")
            
            return view_func(request,username=username, *args, **kwargs)
        except Customuser.DoesNotExist:
            pass
        
        return view_func(request,username=None, *args, **kwargs)
    return wrapper_func

