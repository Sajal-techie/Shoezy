from django.shortcuts import render, redirect
from .models import *
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from user_profile.models import *
from django.views import View


def admorders(request):
    if "users" in request.session:
        return redirect("page_not_found")
    if "admin" in request.session:
        orders = Order.objects.all().order_by("-id")

        search = request.GET.get("search", "")
        if search:
            orders = orders.filter(payment_mode__icontains=search)

        # paginator
        page = request.GET.get("page", 1)
        paginator = Paginator(orders, 10)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        context = {
            "order_items": orders,
            # 'search':search
        }
        return render(request, "admin/admorders.html", context)

    return redirect("admlogin")


def admorderitems(request, id):
    if "users" in request.session:
        return redirect("page_not_found")
    if "admin" in request.session:
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            order = None
        context = {}
        if order is not None:
            order_items = OrderProducts.objects.filter(order_id=order).order_by("-id")
            for order in order_items:
                if order.delivery_date < datetime.now().date() and order.status in [
                    "ordered",
                    "shipped",
                    "out for delivery",
                ]:
                    order.status = "delivered"
                    order.save()
                if order.delivery_date == datetime.now().date() and (
                    order.status == "ordered" or order.status == "shipped"
                ):
                    order.status = "out for delivery"
                    order.save()
            context = {"order_items": order_items}
        return render(request, "admin/admorderitems.html", context)

    return redirect("admlogin")


def update_status(request, id):
    if request.method == "POST":
        status1 = request.POST["status"]
        orders = OrderProducts.objects.get(id=id)
        if orders.status == status1:
            return redirect("admorderitems", orders.order_id.id)
        orders.status = status1

        if status1 == "cancelled":
            orders.product.stock = orders.product.stock + orders.quantity
            orders.product.save()
            if orders.order_id.payment_mode != "Cash on delivery":
                try:
                    wallet = Wallet.objects.get(user_id=orders.user1)
                except Wallet.DoesNotExist:
                    wallet = None
                try:
                    order = Order.objects.get(id=orders.order_id.id)
                except Order.DoesNotExist:
                    order = None
                rtn_amount = orders.amount
                if order is not None:
                    if order.coupon_applied and order.coupon_id:
                        count = OrderProducts.objects.filter(order_id=order).count()
                        deduc = int(order.coupon_id.discount_amount) // count
                        rtn_amount = orders.amount - deduc

                if wallet is not None:
                    wallet.amount = wallet.amount + rtn_amount
                    wallet.save()

        if status1 == "delivered" or status1 == "out for delivery":
            orders.delivery_date = datetime.now().date()
        orders.save()
    return redirect("admorderitems", orders.order_id.id)


def update_date(request, id):
    if request.method == "POST":
        new_date1 = request.POST["date"]
        new_date = datetime.strptime(new_date1, "%Y-%m-%d").date()
        orders = OrderProducts.objects.get(id=id)

        if new_date < orders.order_id.order_date:
            messages.error(request, "Delivery date must be after order date")
            return redirect("admorderitems", orders.order_id.id)

        orders.delivery_date = new_date
        orders.save()

    return redirect("admorderitems", orders.order_id.id)


class Return_management(View):
    success_url = "admin/view_returns.html"

    def get(self, request, *args, **kwargs):
        try:
            if "admin" in request.session:
                returns = Returns.objects.all().order_by("-id")
                context = {"returns": returns}
                return render(request, "admin/view_returns.html", context)
            return redirect("admlogin")
        except Exception as e:
            print(e)
        return redirect("admlogin")

    def post(self, request):
        try:
            ret_id = request.POST.get("id")
            status = request.POST.get("status", None)
            date = request.POST.get("date", None)
            try:
                ret = Returns.objects.get(id=ret_id)
                if status:
                    ret.order.status = status
                    if status == "return accepted":
                        ret.return_date = datetime.now().date() + timedelta(7)
                        ret.order.product.stock = (
                            ret.order.product.stock + ret.order.quantity
                        )
                        ret.order.product.save()
                        if ret.order.order_id.payment_mode != "Cash on delivery":
                            try:
                                wallet = Wallet.objects.get(user_id=ret.user)
                            except Wallet.DoesNotExist:
                                wallet = None
                            try:
                                order = Order.objects.get(id=ret.order.order_id.id)
                            except Order.DoesNotExist:
                                order = None
                            rtn_amount = ret.order.amount
                            if order is not None:
                                if order.coupon_applied and order.coupon_id:
                                    count = OrderProducts.objects.filter(
                                        order_id=order
                                    ).count()
                                    deduc = (
                                        int(order.coupon_id.discount_amount) // count
                                    )
                                    rtn_amount = ret.order.amount - deduc

                            if wallet is not None:
                                wallet.amount = wallet.amount + rtn_amount
                                wallet.save()

                if date:
                    date = datetime.strptime(date, "%Y-%m-%d").date()
                    print(date)
                    ret.return_date = date
                ret.save()
                ret.order.save()
                return redirect("view_returns")

            except Exception as e:
                print(e)

            return redirect("admlogin")
        except Exception as e:
            print(e)
        return redirect("admlogin")
