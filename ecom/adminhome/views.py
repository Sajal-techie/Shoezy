from django.shortcuts import render, redirect
from home.models import Customuser
from django.db.models import Q, F
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from order_management.models import *
from django.db.models.aggregates import Sum, Count
from django.db.models.functions import ExtractMonth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@never_cache
def admlogin(request):
    if "users" in request.session:
        return redirect("page_not_found")
    if "admin" in request.session:
        return redirect("admhome")
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]

        user = authenticate(username=name, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            request.session["admin"] = name
            return redirect("admhome")
        else:
            messages.error(request, "invalid username or password")
            return redirect("admlogin")

    return render(request, "admin/admlogin.html")


@never_cache
@login_required(login_url="admlogin")
def admhome(request):
    if "users" in request.session:
        return redirect("page_not_found")
    if "admin" in request.session:
        if request.user.is_staff:
            if request.method == "POST":
                date1 = request.POST["date1"]
                date2 = request.POST["date2"]
                if date1 > date2:
                    messages.error(request, "Start date must be less than End date")
                    return redirect("admhome")
                orders = OrderProducts.objects.filter(
                    Q(order_id__order_date__range=(date1, date2))
                    & Q(status="delivered")
                    | Q(status="return denied")
                )

                context = {"orders": orders}
                return render(request, "admin/sales.html", context)
            today = datetime.now().date()
            yesterday = datetime.now().date() - timedelta(1)
            this_week = today - timedelta(7)
            last_week = this_week - timedelta(7)
            this_month = today.replace(day=1)
            last_month_last_day = this_month - timedelta(1)
            last_month_first_day = last_month_last_day.replace(day=1)
            this_year = today.replace(day=1, month=1)
            this_year_end = today.replace(day=31, month=12)
            last_year_last_day = this_year - timedelta(1)
            last_year_first_day = last_year_last_day.replace(day=1, month=1)

            daily = (
                OrderProducts.objects.filter(order_id__order_date=today)
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .aggregate(daily=Sum("amount"))["daily"] or 0
            )
            yesterday = (
                OrderProducts.objects.filter(order_id__order_date=yesterday)
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .aggregate(yesterday=Sum("amount"))["yesterday"] or 0
            )
            try:
                daily_perc = -round((((yesterday - daily) / yesterday) * 100), 2)
            except ZeroDivisionError:
                daily_perc = 0

            weekly_sales = (
                OrderProducts.objects.filter(order_id__order_date__gte=this_week)
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .aggregate(weekly_sales=Sum("amount"))["weekly_sales"] or 0
            )
            last_week_sales = (
                OrderProducts.objects.filter(order_id__order_date__gte=last_week)
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .aggregate(last_week_sales=Sum("amount"))["last_week_sales"] or 0
            )
            try:
                weekly_perc = -round(
                    (((last_week_sales - weekly_sales) / last_week_sales) * 100), 2
                )
            except ZeroDivisionError:
                weekly_perc = 0

            monthly_sales = (
                OrderProducts.objects.filter(order_id__order_date__gte=this_month)
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .aggregate(monthly_sales=Sum("amount"))["monthly_sales"] or 0
            )
            last_month_sales = (
                OrderProducts.objects.filter(
                    order_id__order_date__range=(
                        last_month_first_day,
                        last_month_last_day,
                    )
                )
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .aggregate(last_month_sales=Sum("amount"))["last_month_sales"] or 0
            )
            try:
                monthly_perc = -round(
                    (((last_month_sales - monthly_sales) / last_month_sales) * 100), 2
                )
            except ZeroDivisionError:
                monthly_perc = 0

            yearly_sales = (
                OrderProducts.objects.filter(order_id__order_date__gte=this_year)
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .aggregate(yearly_sales=Sum("amount"))["yearly_sales"] or 0
            )
            last_year_sales = (
                OrderProducts.objects.filter(
                    order_id__order_date__range=(
                        last_year_first_day,
                        last_year_last_day,
                    )
                )
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .aggregate(last_year_sales=Sum("amount"))["last_year_sales"] or 0
            )
            try:
                yearly_perc = -round(
                    (((last_year_sales - yearly_sales) / last_year_sales) * 100), 2
                )
            except ZeroDivisionError:
                yearly_perc = 0

            labels = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]
            monthly_sales_data = (
                OrderProducts.objects.filter(
                    order_id__order_date__gte=this_year,
                    order_id__order_date__lte=this_year_end,
                )
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .values(month=ExtractMonth("order_id__order_date"))
                .annotate(monthly_sales=Sum("amount"))
                .order_by("month")
            )

            data = [0] * 12
            for item in monthly_sales_data:
                month_index = item["month"] - 1
                data[month_index] = int(item["monthly_sales"])

            order_status_data = OrderProducts.objects.values("status").annotate(
                status_count=Count("status")
            )
            pielabel = []
            piedata = []
            for item in order_status_data:
                pielabel.append(item["status"])
                piedata.append(item["status_count"])

            last_10_days = [today - timedelta(days=i) for i in range(9, -1, -1)]
            daily_sales_data = (
                OrderProducts.objects.filter(order_id__order_date__in=last_10_days)
                .exclude(Q(status="cancelled") | Q(status="return accepted"))
                .values(orderdate=F("order_id__order_date"))
                .order_by("-orderdate")
                .annotate(daily_sales=Sum("amount"))
            )

            sales_dict = {
                item["orderdate"]: item["daily_sales"] for item in daily_sales_data
            }
            sales_data_filled = [
                {"orderdate": date, "daily_sales": sales_dict.get(date, 0)}
                for date in last_10_days
            ]
            newdata = []
            newlabel = []
            for i in sales_data_filled:
                newdata.append(i["orderdate"])
                newlabel.append(int(i["daily_sales"]))
            newdata = [date.strftime("%Y-%m-%d") for date in newdata]

            context = {
                "daily": daily,
                "weekly_sales": weekly_sales,
                "monthly_sales": monthly_sales,
                "yearly_sales": yearly_sales,
                "daily_perc": daily_perc,
                "weekly_perc": weekly_perc,
                "monthly_perc": monthly_perc,
                "yearly_perc": yearly_perc,
                "labels": labels,
                "data": data,
                "pielabel": pielabel,
                "piedata": piedata,
                "newdata": newdata,
                "newlabel": newlabel,
            }
            return render(request, "admin/admhome.html", context)
        else:
            messages.error(request, "you have no permission to view this page")
            return redirect("admlogin")

    return render(request, "admin/admlogin.html")


def admusers(request):
    if "users" in request.session:
        return redirect("page_not_found")
    if "admin" in request.session and request.user.is_staff:
        user_list = Customuser.objects.all().order_by("id")

        searchs = request.GET.get("searchuser")
        if searchs:
            user_list = user_list.filter(
                Q(first_name__icontains=searchs)
                | Q(last_name__icontains=searchs)
                | Q(email__icontains=searchs)
            ).order_by("id")

        # paginator
        page = request.GET.get("page", 1)
        paginator = Paginator(user_list, 10)
        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            user_list = paginator.page(1)
        except EmptyPage:
            user_list = paginator.page(paginator.num_pages)

        context = {"user_details": user_list}
        return render(request, "admin/admusers.html", context)
    return redirect("admlogin")


def block_user(request, id):
    block = Customuser.objects.get(id=id)
    if not block.is_blocked:
        block.is_blocked = True
        messages.success(request, F" Blocked {block} Successfully ")
        block.save()
        return redirect("admusers")
    return redirect("admusers")


def unblock_user(request, id):
    unblock = Customuser.objects.get(id=id)
    if unblock.is_blocked:
        unblock.is_blocked = False
        messages.success(request, F" Unblocked {unblock} Successfully ")
        unblock.save()
        return redirect("admusers")
    return redirect("admusers")


def sales_report(request):
    if "admin" in request.session:
        context = {}
        if request.method == "POST":
            date1 = request.POST["date1"]
            date2 = request.POST["date2"]
            if date1 > date2:
                messages.error(request, "Start date must be less than End date")
                return redirect("admhome")
            orders = OrderProducts.objects.filter(
                Q(order_id__order_date__range=(date1, date2)) & Q(status="delivered")
                | Q(status="return denied")
            )

            context = {"orders": orders}
            return render(request, "admin/sales.html", context)
        return render(request, "admin/sales.html", context)
    return redirect("admlogin")




def admlogout(request):
    if "admin" in request.session:
        del request.session["admin"]

    return redirect("admlogin")
