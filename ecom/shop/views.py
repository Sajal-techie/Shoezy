from django.shortcuts import render, redirect
from home.models import Customuser
from django.views.decorators.cache import never_cache
from productmanagement.models import *
from django.contrib import messages
from categorymanagement.models import Brand
from cart.views import  check_wishlist
from cart.models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from user_profile.models import ProductReview
from django.db.models import Count, Sum
from order_management.models import OrderProducts


def shop(request):
    try:
        context = {}
        try:
            products = Product.objects.filter(
                is_listed=True, brand_id__is_listed=True
            ).order_by("-id")
        except Product.DoesNotExist:
            products = None
        try:
            brands = Brand.objects.filter(is_listed=True).order_by("id")
        except Product.DoesNotExist:
            brands = None

        # paginator
        page = request.GET.get("page", 1)

        # list all available color and size
        try:
            color_list = ProductVariant.objects.values("color").distinct()
        except ProductVariant.DoesNotExist:
            color_list = None

        try:
            size_list = ProductVariant.objects.values("size").distinct()
        except ProductVariant.DoesNotExist:
            size_list = None
        
        #  filtering products
        try:
            men = request.GET.get("men")
            women = request.GET.get("women")
            brand_names = request.GET.getlist("brandname")
            color_names = request.GET.getlist("colors")
            sizes = request.GET.getlist("size")
            discount = request.GET.get("dis")
            lowest = request.GET.get("lowest")
            highest = request.GET.get("highest")
            sortby = request.GET.get("sort_by")
            itm = request.GET.get("search_items")

            if itm:
                products = products.filter(
                    Q(Q(name__icontains=itm.strip()) | Q(brand__brand_name__icontains=itm.strip()))
                )
            context["srcitem"] = itm

            if men and women:
                products = products.filter(
                    Q(category=men) | Q(category=women) | Q(category="all")
                ).order_by("-id")
            elif women:
                products = products.filter(category=women).order_by("-id")
            elif men:
                products = products.filter(category=men).order_by("-id")
            context["men"] = men
            context["women"] = women

            if brand_names:
                products = products.filter(
                    brand_id__brand_name__in=brand_names
                ).order_by("-id")
            context["brand_names"] = brand_names

            if color_names:
                products = products.filter(
                    productvariant__color__in=color_names
                ).distinct()
            context["color_names"] = color_names

            if sizes:
                products = products.filter(productvariant__size__in=sizes).distinct()
            context["sizes"] = sizes

            if discount:
                products = products.filter(discount_percentage__gte=discount)
            context["discount"] = discount

            if lowest and highest:
                if int(lowest) > int(highest):
                    messages.error(
                        request, "Starting prize must be less than Highest prize"
                    )

                products = products.filter(selling_price__range=(lowest, highest))
            elif lowest:
                products = products.filter(selling_price__gte=lowest)
            elif highest:
                products = products.filter(selling_price__lte=highest)

            context["lowest"] = lowest
            context["highest"] = highest

            if sortby:
                if sortby == "price_high":
                    products = products.order_by("-selling_price")
                elif sortby == "price_low":
                    products = products.order_by("selling_price")

            context["sort_by"] = sortby

            paginator = Paginator(products, 9)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            context["product"] = products
            context["brand"] = brands
            context["color_list"] = color_list
            context["size_list"] = size_list

        except Exception as e:
            print(e)

        if "users" in request.session:
            usm = request.session.get("users")
            try:
                username = Customuser.objects.get(email=usm)
            except Customuser.DoesNotExist:
                username = None

            context["username"] = username
            wishlist1 = []
            wishitems = Wishlist.objects.filter(user_id=username)
            for j in wishitems:
                wishlist1.append(j.product_id.id)
            context["wishlist1"] = wishlist1
            if not username.is_blocked:
                return render(request, "shop/shop.html", context)
            else:
                if "users" in request.session:
                    del request.session["users"]
                messages.error(request, "you are blocked ")
                return redirect("login")

    except Exception as e:
        print(e)

    return render(request, "shop/shop.html", context)


def singleproduct(request, id):
    try:
        products = Product.objects.filter(id=id)
        sproduct = Product.objects.get(id=id)
        brands = Brand.objects.filter(id=id)
        multiple = ProductImages.objects.filter(product_id=id)
        productvariant = ProductVariant.objects.filter(product_id=id)[:1]
        productvariants = ProductVariant.objects.filter(product_id=id)
        prodsize = productvariants.values("size").order_by("size")
        review = ProductReview.objects.filter(product=sproduct).order_by("-rating")
        review_count = review.aggregate(num_reviews=Count("id"))["num_reviews"]
        sum_rating = review.aggregate(sum_rat=Sum("rating"))["sum_rat"]
        try: 
            avg_rating = sum_rating / review_count if review_count else 0
        except ZeroDivisionError:
            avg_rating = 0
        order_count = OrderProducts.objects.filter(
            Q(product__product_id=sproduct) & 
                (Q (status="delivered") |Q(status="return denied") | 
                Q(status="return request") | Q(status="return accepted"))
        ).count()
        context = {
            "product": products,
            "brand": brands,
            "multi_image": multiple,
            "productvariant": productvariant,
            "productvariants": productvariants,
            "reviews": review,
            "review_count": review_count,
            "avg_rating": avg_rating,
            "order_count": order_count,
            'prodsize':prodsize,
        }
        if "users" in request.session:
            usm = request.session.get("users")
            username = Customuser.objects.get(email=usm)
            if username.is_blocked:
                if "users" in request.session:
                    del request.session["users"]
                messages.error(request, "you are blocked ")
                return redirect("login")
            is_in_wish = check_wishlist(username, id)
            context["is_in_wish"] = is_in_wish
            context["username"] = username

            if not username.is_blocked:
                return render(request, "shop/singleproduct.html", context)
            else:
                if "users" in request.session:
                    del request.session["users"]
                messages.error(request, "you are blocked ")

                return redirect("login")
        return render(request, "shop/singleproduct.html", context)
    except Exception as e:
        print(e)

    return render(request, "shop/shop.html")


# resetting filters
def reset_filters(request):
    return redirect("shop")
