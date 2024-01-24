from cart.models import Cart,Wishlist
from home.models import Customuser

def cart_count(request):
    cont = {'cart_count':0,
            'wish_count':0}
    if 'users' in request.session:
        usm = request.session.get('users')
        username = Customuser.objects.get(email = usm)
        cart_count = Cart.objects.filter(user_id = username).count()
        wish_count = Wishlist.objects.filter(user_id = username).count()
        cont = {
            'cart_count':cart_count,
            'wish_count':wish_count,
            'username':username
        }
    return cont
 

