from django.shortcuts import render, redirect
from .models import *
from .forms import Adressform
from home.models import Customuser
from order_management.models import *
from django.views.decorators.cache import never_cache, cache_control
from django.contrib import messages
from cart.models import *
from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime
from home.decorator import session_handler

@session_handler
def view_profile(request, username=None):
    try:
        if username:
            try:
                addressess = Address.objects.filter(
                    Q(user=username) & Q(is_available=True)
                )

                try:
                    wallet = Wallet.objects.get(user_id=username)
                except Wallet.DoesNotExist:
                    wallet = None

            except Exception as e:
                print(e)

            context = {"username": username, "address": addressess, "wallet": wallet}
            return render(request, "profile/user_details.html", context)

    except Exception as e:
        print(e)
        return redirect("home")

    return redirect("login")


@never_cache
def edit_profile(request, id):
    try:
        try:
            username = Customuser.objects.get(id=id)
        except Customuser.DoesNotExist:
            username = None

        context = {
            "username": username,
        }
        if request.method == "POST":
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            number = request.POST["number"]
            gender = request.POST["gender"]
            dob = request.POST["dob"]

            # check if the dob is null or not and change the dob
            if dob != "":
                date_obj = date.fromisoformat(dob)
                eighteen = timezone.now().date() - timezone.timedelta(365 * 18)
                if date_obj > eighteen:
                    messages.error(
                        request,
                        "You do not meet the age requirements.(minimum 18 years old)",
                    )
                    return redirect("edit_profile", id)
                else:
                    username.dob = date_obj

            if not number == "" and len(number) != 10:
                messages.error(request, "Enter valid number")
                return redirect("edit_profile", id)

            username.first_name = fname
            username.last_name = lname
            username.number = number
            username.gender = gender
            username.save()
            messages.success(request, "Profile Updated ")
            return redirect("view_profile")
        return render(request, "profile/edit_profile.html", context)

    except Exception as e:
        print(e)

    return redirect("view_profile")


# reset password from profile after logging in
@session_handler
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
def reset_password(request, username=None):
    try:
        if username:

            context = {}

            if request.method == "POST":
                old = request.POST["old_pass"]
                new = request.POST["new_pass"]
                new1 = request.POST["new_pass1"]
                if username.password == old:
                    if len(new) < 6:
                        messages.error(
                            request, "password must be more than 6 characters"
                        )
                        return redirect("reset_password")
                    if new != new1:
                        messages.error(request, "passwords must be equal")
                        return redirect("reset_password")

                    username.password = new
                    username.save()
                    messages.success(request, "Password changed successfully")
                    return redirect("view_profile")
                else:
                    messages.error(request, "incorrect password")
                    return redirect("reset_password")

            return render(request, "profile/reset_password.html", context)

    except Exception as e:
        print(e)
        return redirect("view_profile")
    return redirect("login")


@session_handler
def add_address(request, username=None):
    try:
        if username:
            if request.method == "POST":
                try:
                    form = Adressform(request.POST)
                except Exception as e:
                    print(e)

                if form.is_valid():
                    address = form.save(commit=False)

                    if len(address.number) != 10:
                        messages.error(request, "Enter valid number")
                        return redirect("add_address")

                    if address.pincode >= 999999:
                        messages.error(request, "enter valid pincode")
                        return redirect("add_address")

                    address.user = username
                    address.save()
                    next_url = request.GET.get("next", None)
                    messages.success(request, "New Address added successfully")
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect("home")
            else:
                form = Adressform()
            return render(
                request,
                "profile/add_address.html",
                {"form": form, "username": username},
            )
    except Exception as e:
        print(e)
        return redirect("view_profile")
    return redirect("login")


def edit_address(request, id):
    try:
        existing_address = Address.objects.get(id=id)
    except Address.DoesNotExist:
        existing_address = None

    if request.method == "POST":
        form = Adressform(request.POST, instance=existing_address)
        if form.is_valid():
            address = form.save(commit=False)

            if len(address.number) != 10:
                messages.error(request, "Enter valid number")
                return redirect("add_address")

            if address.pincode >= 999999:
                messages.error(request, "enter valid pincode")
                return redirect("add_address")

            address.save()
            messages.success(request, "Updated the Address successfully")
            return redirect("view_profile")
    else:
        form = Adressform(instance=existing_address)

    return render(request, "profile/edit_address.html", {"form": form, "address": id})


def delete_address(request, id):
    try:
        address = Address.objects.get(id=id)
    except Address.DoesNotExist:
        address = None

    address.is_available = False
    address.save()
    messages.success(request, "Deleted the Address successfully")
    return redirect("view_profile")


# for showing order history (Order)
@session_handler
def order_history(request, username=None):
    try:
        if username:
            try:
                order_items = Order.objects.filter(user=username).order_by("-id")

            except Exception as e:
                print(e)

            context = {
                "order_items": order_items,
                "username": username,
            }
            return render(request, "profile/order_history.html", context)

    except Exception as e:
        print(e)
        return redirect("home")
    return redirect("login")


# for shwowing order history products(OrderProducts)
@session_handler
def order_history_items(request, id, username=None):
    if username:
        try:
            order = Order.objects.get(id=id)
            order_items = OrderProducts.objects.filter(order_id=order)

            context = {
                "order_items": order_items,
                "order": order,
            }

            return render(request, "profile/order_history_items.html", context)

        except Exception as e:
            print(e)
            return redirect("order_history")
    else:
        return redirect("login")


@session_handler
def track_order(request, id, username=None):
    try:
        if username:
            try:
                order_items = OrderProducts.objects.get(id=id)
            except OrderProducts.DoesNotExist:
                order_items = None
            try:
                full_order_items = Order.objects.get(id = order_items.order_id.id)
            except Exception :
                full_order_items = None
                
            if full_order_items is not None:
                rtn_amount = order_items.amount

                if full_order_items.coupon_applied and full_order_items.coupon_id:
                    count = OrderProducts.objects.filter(
                        order_id=full_order_items
                                    ).count()
                    deduc = int(full_order_items.coupon_id.discount_amount) // count
                    rtn_amount = order_items.amount - deduc

            if (
                order_items.status == "return request"
                or order_items.status == "return accepted"
            ):
                tracking_steps = [
                    {"description": "return request"},
                    {"description": "return accepted"},
                ]
            elif order_items.status == "return denied":
                tracking_steps = [
                    {"description": "return request"},
                    {"description": "return denied"},
                ]
            else:
                tracking_steps = [
                    {"description": "ordered"},
                    {"description": "shipped"},
                    {"description": "out for delivery"},
                    {"description": "delivered"},
                ]
            current_status = order_items.status
            current_step_index = next(
                (
                    i
                    for i, step in enumerate(tracking_steps)
                    if step["description"] == current_status
                ),
                None,
            )
            previous_steps = tracking_steps[: current_step_index + 1]
            try:
                review = ProductReview.objects.get(
                    product=order_items.product.product_id, user=username
                )
            except Exception as e:
                review = None

            context = {
                "order": order_items,
                "tracking_steps": tracking_steps,
                "previous_steps": previous_steps,
                "username": username,
                "review": review,
                "rtn_amount":rtn_amount
            }
            try:
                return_item = Returns.objects.get(user=username, order=order_items)
                context["returns"] = return_item
            except Exception as e:
                print(e)
                return_item = None
            return render(request, "profile/track_order.html", context)

    except Exception as e:
        print(e)
        return redirect("order_history")
    return redirect("login")


@session_handler
def cancel_order(request, id,username=None):
    try:
        if username:
            try:
                current_order = OrderProducts.objects.get(id=id)
            except OrderProducts.DoesNotExist:
                current_order = None

            if request.method == "POST":
                reason = request.POST.get("reason", "")
                if not reason.strip():
                    messages.error(request, "Enter a valid reason ")
                    return redirect("track_order", id)
                
                if current_order.status != "delivered":
                    current_order.status = "cancelled"
                    current_order.reason = reason
                    current_order.delivery_date = timezone.now()
                    current_order.save()
                    current_order.product.stock = (
                        current_order.product.stock + current_order.quantity
                    )
                    current_order.product.save()

                    if current_order.order_id.payment_mode != "Cash on delivery":
                        try:
                            wallet = Wallet.objects.get(user_id=username)
                        except Wallet.DoesNotExist:
                            wallet = None
                        try:
                            order = Order.objects.get(id=current_order.order_id.id)
                        except Order.DoesNotExist:
                            order = None
                        if order is not None:
                            rtn_amount = current_order.amount
                            if order.coupon_applied and order.coupon_id:
                                count = OrderProducts.objects.filter(
                                    order_id=order
                                ).count()
                                deduc = int(order.coupon_id.discount_amount) // count
                                rtn_amount = current_order.amount - deduc

                        if wallet is not None:
                            wallet.amount = wallet.amount + rtn_amount
                            wallet.save()
                            
                            messages.success(request, F"Order id : {current_order.id} cancelled  ")
                            messages.success(request, F"{rtn_amount} refunded to wallet ")
                            
                    else:
                        messages.success(request, F" Order id: {current_order.id}  cancelled successfully ")
                    return redirect("order_history_items", current_order.order_id.id)
            return redirect("order_history_items", current_order.order_id.id)

    except Exception as e:
        print(e)
        return redirect("order_history")

    return redirect("login")


# for showing order details for single product
@session_handler
def view_order_details(request, id, username=None):
    try:
        if username:
            try:
                order = OrderProducts.objects.get(id=id)
            except OrderProducts.DoesNotExist:
                order = None
            
            try:
                returns = Returns.objects.get(order = order)
            except Returns.DoesNotExist or Returns.MultipleObjectsReturned:
                returns = None

            context = {
                "username": username,
                "order_item": order,
                "returns":returns
            }

            return render(request, "profile/view_order_details.html", context)

    except Exception as e:
        print(e)
        return redirect("order_history_items", order.order_id.id)
    return redirect("login")


@session_handler
def order_invoice(request, id, username=None):
    try:
        if username:
            try:
                order_item = OrderProducts.objects.get(id=id)
            except Exception:
                order_item = None
            if order_item is not None:
                current_date = datetime.now().date()
                context = {"item": order_item, "date": current_date}
            return render(request, "profile/invoice.html", context)
        return redirect("login")
    except Exception as e:
        print(e)
    return redirect("track_order", id)


# add review for delivered products
@session_handler
def add_review(request, pid, oid, username=None):
    try:
        if username:
            try:
                product = Product.objects.get(id=pid)
            except Exception as e:
                product = None
                print(e)
                return redirect("track_order", oid)
            if request.method == "POST":
                review = request.POST["review"]
                rating = request.POST["rating"]
                review = str(review).strip()
                
                if int(rating) == 0:
                    messages.error(request, "Enter valid rating (minimum 1 star)")
                    return redirect("track_order", id=oid)
                
                if ProductReview.objects.filter(
                    product=product, user=username
                ).exists():
                    messages.error(request, "You already added a review")
                    return redirect("track_order", id=oid)
                ProductReview.objects.create(
                    product=product, user=username, rating=rating, review=review
                )
                messages.success(request, "Review added succesfully")
                return redirect("track_order", id=oid)

            return redirect("track_order", id=oid)

        return redirect("login")
    except Exception as e:
        print(e)
    return redirect("home")


# edit review
@session_handler
def update_review(request, pid, oid, username=None):
    try:
        if username:
            try:
                product = Product.objects.get(id=pid)
            except Exception as e:
                product = None
                print(e)
                return redirect("track_order", oid)
            
            if request.method == "POST":
                reviews = request.POST["review"]
                rating = request.POST["rating"]
                reviews = str(reviews).strip()
                
                if int(rating) == 0:
                    messages.error(request, "enter valid Rating (minimum 1 star) ") 
                    return redirect("track_order", id=oid)
                try:
                    review = ProductReview.objects.get(product=product, user=username)
                except Exception as e:
                    review = None
                
                if review is not None:
                    review.review = reviews
                    review.rating = rating
                    review.save()
                    messages.success(request, "Review Updated succesfully")

                return redirect("track_order", id=oid)

            return redirect("track_order", id=oid)

        return redirect("login")
    except Exception as e:
        print(e)
    return redirect("home")


@session_handler
def return_request(request, id,username=None):
    try:
        if username:
            try:
                order = OrderProducts.objects.get(id=id)
            except Exception as e:
                print(e)
                order = None
            if request.method == "POST":
                reason = request.POST.get("reason", "")
                
                if not reason.strip():
                    messages.error(request, "enter a valid reason ")
                    return redirect("track_order", id)
                
                if order is not None:
                    Returns.objects.create(order=order, user=order.user1, reason=reason.strip())
                    order.status = "return request"
                    order.save()
                    messages.success(request, "Requested for return ")
            return redirect("track_order", id)
    except Exception as e:
        print(e)
    return redirect("home")
