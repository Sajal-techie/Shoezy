from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from home.models import Customuser
from productmanagement.models import *
from .models import *
from user_profile.models import *
from order_management.models import *
from django.utils import timezone
from django.db.models import F 
from home.decorator import session_handler

@session_handler
def cart(request, username = None):
    if username:
        if username.is_blocked:
            if "users" in request.session:
                del request.session["users"]
            messages.error(request, "you are blocked ")
            return redirect("login")
        cart_items = (
            Cart.objects.filter(user_id=username)
            .select_related("product__product_id__brand")
            .order_by("-id")
        )
        for i in cart_items:
            i.save()
        total = sum(i.sub_total for i in cart_items)
        context = {
            "username": username,
            "cart_item": cart_items,
            "total": total,
        }

        if not username.is_blocked:
            return render(request, "cart/cart.html", context)

    messages.error(request, "you need to login")
    return redirect("login")


@session_handler
def addto_cart(request, p_id, username=None):
    if username:
        next_url = request.GET.get("next", None)
        if next_url is not None:
            product = Product.objects.get(id=p_id)
        else:
            product = Product.objects.get(productvariant__id=p_id)
        size = request.GET.get("size", None)
        quantity = int(request.GET.get("quantity", 1))
        try:
            product_size = ProductVariant.objects.get(product_id=product, size=size)
        except ProductVariant.DoesNotExist:
            product_size = None

        if product_size is None:
            messages.error(request, "Not available")
            if next_url is not None:
                return redirect(next_url)
            return redirect("singleproduct", product.id)

        if product_size.stock < quantity:
            messages.error(request, "out of Stock")
            if next_url is not None:
                return redirect(next_url)
            return redirect("singleproduct", product.id)

        if product_size.stock > 0:
            if not Cart.objects.filter(
                user_id=username, product=product_size, size=size
                    ).exists():
                Cart.objects.create(
                    user_id=username, product=product_size, size=size, quantity=quantity
                )
                
                # removing from wishlist if added to cart
                if next_url is not None:
                        Wishlist.objects.filter(product_id = product).delete()
                messages.success(
                    request, f"{product.name} size({product_size.size}) added to Cart "
                )
            else:
                messages.error(
                    request, f"{product.name} size({product_size.size}) Already in Cart"
                )
        else:
            messages.error(request, "Out of stock")
        if next_url is not None:
            return redirect(next_url)
        return redirect("singleproduct", product.id)
    messages.error(request, "you need to login")
    return redirect("login")



def check_wishlist(user, product_id):
    is_in_wish = Wishlist.objects.filter(user_id=user, product_id=product_id).exists()
    return is_in_wish


def change_quantity(request):
    if request.method == "POST":
        products_id = int(request.POST.get("products_id"))
        action = request.POST.get("action")
        item = Cart.objects.get(id=products_id)

        if action == "plus":
            if item.quantity < item.product.stock and item.quantity < 5:
                item.quantity = item.quantity + 1
        elif action == "minus":
            if item.quantity > 1:
                item.quantity = item.quantity - 1

        item.sub_total = item.product.product_id.selling_price * item.quantity
        item.save()
        return JsonResponse({"status": "updated suucessfully"})


def remove_cart(request, id):
    try:
        remove_item = Cart.objects.get(id=id)
    except Cart.DoesNotExist:
        remove_item = None
    if remove_item is not None:
        remove_item.delete()
        messages.success(request, " item removed from cart ")
    return redirect("cart")


@session_handler
def checkout(request, username=None):
    if username:
        address = Address.objects.filter(user=username.id, is_available=True).order_by(
            "id"
        )
        cart_items = Cart.objects.filter(user_id=username.id).select_related(
            "product__product_id"
        )
        for i in cart_items:
            if i.product.stock < i.quantity:
                messages.error(request, f'{i.product.product_id.name}({i.product.size}) out of stock')
                
                return redirect('cart')
            
        total = sum(i.sub_total for i in cart_items)
        wallet = Wallet.objects.get(user_id=username)
        try:
            checkout = Checkout.objects.get(user_id=username)
            checkout.sub_total = total
            checkout.payable_amount = total
            checkout.save()
            if checkout.coupon_active:
                checkout.payable_amount = (
                    float(checkout.sub_total) - checkout.discount_amount
                )
                total = float(checkout.sub_total) - checkout.discount_amount
                checkout.save()

        except Checkout.DoesNotExist:
            checkout = Checkout(user_id=username, sub_total=total, payable_amount=total)
            checkout.save()
        context = {
            "address": address,
            "cart_items": cart_items,
            "username": username,
            "total": total,
            "checkout": checkout,
            "wallet": wallet,
        }
        if request.method == "POST":
            adress1 = request.POST.get("address", None)
            if not adress1:
                messages.error(request, "add address for delivery")
                return redirect("checkout")
            payment = "Cash on delivery"
            adress = Address.objects.get(id=adress1)
            if checkout.coupon_active:
                current_order = Order.objects.create(
                    user=username,
                    address=adress,
                    total=total,
                    payment_mode=payment,
                    coupon_applied=True,
                    coupon_id=checkout.coupon,
                    og_amount=checkout.sub_total,
                )
            else:
                current_order = Order.objects.create(
                    user=username,
                    address=adress,
                    total=total,
                    payment_mode=payment,
                    coupon_applied=False,
                    coupon_id=None,
                    og_amount=total,
                )
            for i in cart_items:
                obj = OrderProducts(
                    order_id=current_order,
                    user1=username,
                    product=i.product,
                    address1=adress,
                    quantity=i.quantity,
                    amount=i.sub_total,
                    status="ordered",
                    size=i.size,
                )
                if obj.product.stock > 0:
                    obj.product.stock = obj.product.stock - obj.quantity
                    obj.product.save()
                else:
                    messages.error(request, "out of stock")
                    return redirect("checkout")
                obj.save()
                i.delete()
            checkout.delete()
            return redirect("confirm", current_order.id)

        return render(request, "cart/checkout.html", context)

    return redirect("login")


@session_handler
def apply_coupon(request, username=None):
    if username:
        orders = Order.objects.filter(user=username)
        checkouted = Checkout.objects.get(user_id=username)
        if request.method == "POST":
            code = request.POST.get("code")
            try:
                coupons = Coupen.objects.get(code=code)
            except Coupen.DoesNotExist:
                checkouted.coupon_active = False
                checkouted.discount_amount = 0
                checkouted.coupon = None
                checkouted.save()
                coupons = None
                return JsonResponse({"error": "Invalid Coupon code"})
            if coupons is not None:
                today = timezone.now().date()
                if not coupons.is_active:
                    checkouted.coupon_active = False
                    checkouted.coupon = None
                    checkouted.discount_amount = 0
                    checkouted.save()
                    return JsonResponse({"error": "Coupon is not available now"})
                if coupons.valid_from > today:
                    checkouted.coupon_active = False
                    checkouted.coupon = None
                    checkouted.discount_amount = 0
                    checkouted.save()
                    return JsonResponse({"error": "Coupon  not started"})
                if coupons.valid_to < today:
                    checkouted.coupon_active = False
                    checkouted.coupon = None
                    checkouted.discount_amount = 0
                    checkouted.save()
                    return JsonResponse({"error": "Coupon expired"})
                used_coupons = []
                for i in orders:
                    if i.coupon_applied and i.coupon_id is not None:
                        used_coupons.append(i.coupon_id.id)
                if coupons.id in used_coupons:
                    checkouted.coupon_active = False
                    checkouted.coupon = None
                    checkouted.discount_amount = 0
                    checkouted.save()
                    return JsonResponse(
                        {
                            "error": "This coupon has already been used. Please choose another one."
                        }
                    )
                checkouted.payable_amount = (
                    checkouted.sub_total - coupons.discount_amount
                )
                if checkouted.payable_amount < 500:
                    checkouted.coupon_active = False
                    checkouted.coupon = None
                    checkouted.discount_amount = 0
                    checkouted.payable_amount = checkouted.sub_total
                    checkouted.save()
                    return JsonResponse(
                        {"error": "Not available for this order Order more items."}
                    )
                checkouted.coupon_active = True
                checkouted.coupon = coupons
                checkouted.discount_amount = coupons.discount_amount
                checkouted.save()
                return JsonResponse({"success": "Coupon Applied "})
        return JsonResponse({"error": "Invalid request"})


@session_handler
def remove_coupon(request, username=None):
    if username:
        checkouted = Checkout.objects.get(user_id=username)
        if request.method == "POST":
            if checkouted.coupon_active:
                checkouted.coupon_active = False
                checkouted.coupon = None
                checkouted.discount_amount = 0
                checkouted.save()
        return JsonResponse(
                        {"error": " Coupon removed "}
                    )

@session_handler
def razor_pay(request, username=None):
    if username:
        address = Address.objects.filter(user=username.id, is_available=True).order_by(
            "id"
        )
        cart_items = Cart.objects.filter(user_id=username.id).select_related(
            "product__product_id"
        )
        for i in cart_items:
            if i.product.stock < i.quantity:
                messages.error(request, f'{i.product.product_id.name}({i.product.size}) out of stock')
                return redirect('cart')
            
        total = sum(i.sub_total for i in cart_items)
        try:
            checkout = Checkout.objects.get(user_id=username)
        except Checkout.DoesNotExist or Checkout.MultipleObjectsReturned:
            checkout = None
        if request.method == "POST":
            adress1 = request.POST.get("address", None)
            if adress1 is None:
                messages.error(request, "Add a new Address")
                data = {"redirect_url": "/checkout/", "error": True}
                return JsonResponse(data)
            
            payment = "Razorpay"
            adress = Address.objects.get(id=adress1)
            if checkout is not None:
                if checkout.coupon_active:
                    total = checkout.payable_amount
                    current_order = Order.objects.create(
                        user=username,
                        address=adress,
                        total=total,
                        payment_mode=payment,
                        coupon_applied=True,
                        coupon_id=checkout.coupon,
                        og_amount=checkout.sub_total,
                    )
                else:
                    current_order = Order.objects.create(
                        user=username,
                        address=adress,
                        total=total,
                        payment_mode=payment,
                        coupon_applied=False,
                        coupon_id=None,
                        og_amount=total,
                    )
            else:
                current_order = Order.objects.create(
                    user=username,
                    address=adress,
                    total=total,
                    payment_mode=payment,
                    coupon_applied=False,
                    coupon_id=None,
                    og_amount=total,
                )
            for i in cart_items:
                obj = OrderProducts(
                    order_id=current_order,
                    user1=username,
                    product=i.product,
                    address1=adress,
                    quantity=i.quantity,
                    amount=i.sub_total,
                    status="ordered",
                    size=i.size,
                )
                if obj.product.stock > 0:
                    obj.product.stock = obj.product.stock - obj.quantity
                    obj.product.save()
                else:
                    messages.error(request, "out of stock")
                    data = {"redirect_url": "/checkout/", "error": True}
                    return JsonResponse(data)
                obj.save()
                i.delete()
            checkout.delete()
            data = {
                "redirect_url": "/confirm/",
                "order_id1": current_order.id,
                "completed": True,
            }
            return JsonResponse(data)


@session_handler
def wallet_pay(request, username=None):
    if username:
        cart_items = Cart.objects.filter(user_id=username.id).select_related(
            "product__product_id"
        )
        for i in cart_items:
            if i.product.stock < i.quantity:
                messages.error(request, f'{i.product.product_id.name}({i.product.size}) out of stock')
                return redirect('cart')
             
        total = sum(i.sub_total for i in cart_items)
        try:
            checkout = Checkout.objects.get(user_id=username)
            total = checkout.payable_amount
        except Checkout.DoesNotExist or Checkout.MultipleObjectsReturned:
            checkout = None
        if request.method == "POST":
            adress1 = request.POST.get("address", None)
            if adress1 is None:
                messages.error(request, "Add a new Address")
                data = {"redirect_url": "/checkout/", "error": True}
                return JsonResponse(data)
            
            payment = "Wallet"
            adress = Address.objects.get(id=adress1)
            try:
                wallet = Wallet.objects.get(user_id=username)
            except Wallet.DoesNotExist:
                wallet = None
            if wallet is not None:
                wallet.amount = wallet.amount - total
                wallet.save()
            if checkout is not None:
                if checkout.coupon_active:
                    total = checkout.payable_amount
                    current_order = Order.objects.create(
                        user=username,
                        address=adress,
                        total=total,
                        payment_mode=payment,
                        coupon_applied=True,
                        coupon_id=checkout.coupon,
                        og_amount=checkout.sub_total,
                    )
                else:
                    current_order = Order.objects.create(
                        user=username,
                        address=adress,
                        total=total,
                        payment_mode=payment,
                        coupon_applied=False,
                        coupon_id=None,
                        og_amount=total,
                    )
            else:
                current_order = Order.objects.create(
                    user=username,
                    address=adress,
                    total=total,
                    payment_mode=payment,
                    coupon_applied=False,
                    coupon_id=None,
                    og_amount=total,
                )

            for i in cart_items:
                obj = OrderProducts(
                    order_id=current_order,
                    user1=username,
                    product=i.product,
                    address1=adress,
                    quantity=i.quantity,
                    amount=i.sub_total,
                    status="ordered",
                    size=i.size,
                )
                if obj.product.stock > 0:
                    obj.product.stock = obj.product.stock - obj.quantity
                    obj.product.save()
                else:
                    messages.error(request, "out of stock")
                    data = {"redirect_url": "/checkout/", "error": True}
                    return JsonResponse(data)
                obj.save()
                i.delete()
            checkout.delete()
            data = {
                "redirect_url": "/confirm/",
                "order_id1": current_order.id,
                "completed": True,
            }
            return JsonResponse(data)


@session_handler
def confirm(request, id, username=None):
    if username:
        orders = Order.objects.get(id=id)
        order_items = OrderProducts.objects.filter(order_id=id)
        context = {
            "username": username,
            "orders": orders,
            "order_items": order_items,
        }
        return render(request, "cart/confirm.html", context)

    return redirect("login")


@session_handler
def wishlist(request, username=None):
    if username:
        if username.is_blocked:
            if "users" in request.session:
                del request.session["users"]
            messages.error(request, "you are blocked ")
            return redirect("login")
        
        # taking available sizes to show in wishlist
        prodsize = Wishlist.objects.filter(user_id = username).values_list(
                                'product_id__id',('product_id__productvariant__size')
                                ).order_by('product_id__productvariant__size')
        
        wishlist_items = (
            Wishlist.objects.filter(user_id=username)
            .select_related("product_id__brand")
            .order_by("-id")
        )
        context = {
            "username": username,
            "wishlist_items": wishlist_items,
            'prodsize':prodsize
        }
        return render(request, "cart/wishlist.html", context)
    return redirect("login")

@session_handler
def add_to_wish(request, id,username = None): 
    if username: 
        products = Product.objects.get(id=id)
        if not Wishlist.objects.filter(product_id=products, user_id=username):
            wish = Wishlist.objects.create(product_id=products, user_id=username)
            messages.success(request, f"{products.name} added to wishlist")
            wish.save()
        nxt_url = request.GET.get("next", "/")
        return redirect(nxt_url)
    messages.error(request, "you need to login")
    return redirect("login")


@session_handler
def remove_wish(request, id,username=None):
    if username:
        prod = Product.objects.get(id=id)
        wish = Wishlist.objects.get(product_id=prod, user_id=username)
        wish.delete()
        nxt_url = request.GET.get("next", "wishlist")
        messages.success(request, f"{prod.name} removed from wishlist ")
        return redirect(nxt_url)

    return redirect("login")
