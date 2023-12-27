from django.urls import path
from . import views
urlpatterns = [
    path('cart/', views.cart ,name='cart'),
    path('addto_cart/<str:p_id>/', views.addto_cart ,name='addto_cart'),
    path('remove_cart/<str:id>/', views.remove_cart ,name='remove_cart'),
    path('add_quantity/<str:id>/', views.add_quantity ,name='add_quantity'),
    path('rem_quantity/<str:id>/', views.rem_quantity ,name='rem_quantity'),


]

