from django.urls import path
from . import views

urlpatterns = [
    path('view_coupon/', views.view_coupon, name='view_coupon' ),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('update_coupon/<str:id>', views.update_coupon, name='update_coupon'),
    path('activation/<str:id>', views.activation, name='activation'),
    # path('admlogout/', views.admlogout, name='admlogout'),
    
    # path('admbanners/', views.admbanners, name='admbanners'),


]
