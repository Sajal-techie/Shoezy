from django.shortcuts import render

# Create your views here.
def home(request):
    return render (request, 'home1.html')

def login(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')

def verifyreg(request):
    return render(request, 'login/verifyreg.html')