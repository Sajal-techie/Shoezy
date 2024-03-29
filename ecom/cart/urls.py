from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path("addto_cart/<str:p_id>/", views.addto_cart, name="addto_cart"),
    path("remove_cart/<str:id>/", views.remove_cart, name="remove_cart"),
    path("change_quantity/", views.change_quantity, name="change_quantity"),
    path("checkout/", views.checkout, name="checkout"),
    path("razor_pay/", views.razor_pay, name="razor_pay"),
    path("wallet_pay/", views.wallet_pay, name="wallet_pay"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("remove_wish/<str:id>/", views.remove_wish, name="remove_wish"),
    path("add_to_wish/<str:id>/", views.add_to_wish, name="add_to_wish"),
    path("confirm/<str:id>", views.confirm, name="confirm"),
    path("apply_coupon/", views.apply_coupon, name="apply_coupon"),
    path("remove_coupon/", views.remove_coupon, name="remove_coupon"),
]
