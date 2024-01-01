from django.urls import path
from . import views
urlpatterns = [
    path('cart/', views.cart ,name='cart'),
    path('buy_now/<str:id>/', views.buy_now ,name='buy_now'),
    path('addto_cart/<str:p_id>/', views.addto_cart ,name='addto_cart'),
    path('remove_cart/<str:id>/', views.remove_cart ,name='remove_cart'),
    path('add_quantity/<str:id>/', views.add_quantity ,name='add_quantity'),
    path('rem_quantity/<str:id>/', views.rem_quantity ,name='rem_quantity'),
    path('checkout/', views.checkout ,name='checkout'),
    path('wishlist/', views.wishlist ,name='wishlist'),
    path('remove_wish/<str:id>/', views.remove_wish ,name='remove_wish'),
    path('add_to_wish/<str:id>/', views.add_to_wish ,name='add_to_wish'),
    path('confirm/<str:id>', views.confirm ,name='confirm'),


]

