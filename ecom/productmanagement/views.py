from django.shortcuts import render

# Create your views here.
def view_products(request):
    
    return render(request,'admin/admproducts.html')


def add_product(request):
    if request.method == 'POST':
        request.POST['name']
    return render(request,'admin/admproducts.html')

