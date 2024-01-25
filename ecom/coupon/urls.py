from django.urls import path
from . import views

urlpatterns = [
    path("view_coupon/", views.view_coupon, name="view_coupon"),
    path("add_coupon/", views.add_coupon, name="add_coupon"),
    path("update_coupon/<str:id>", views.update_coupon, name="update_coupon"),
    path("activation/<str:id>", views.activation, name="activation"),
    path("view_brand_offers/", views.view_brand_offers, name="view_brand_offers"),
    path("add_brand_offer/", views.add_brand_offer, name="add_brand_offer"),
    path(
        "update_brand_offer/<str:id>",
        views.update_brand_offer,
        name="update_brand_offer",
    ),
    path(
        "active_brand_offer/<str:id>",
        views.active_brand_offer,
        name="active_brand_offer",
    ),
    path("view_product_offers/", views.view_product_offers, name="view_product_offers"),
    path("add_product_offer/", views.add_product_offer, name="add_product_offer"),
    path(
        "update_product_offer/<str:id>",
        views.update_product_offer,
        name="update_product_offer",
    ),
    path(
        "active_product_offer/<str:id>",
        views.active_product_offer,
        name="active_product_offer",
    ),
]
