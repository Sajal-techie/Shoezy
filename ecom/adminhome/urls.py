from django.urls import path

from . import views
urlpatterns = [
    path('admlogin/', views.admlogin, name='admlogin' ),
    path('admhome/', views.admhome, name='admhome'),
    path('admusers/', views.admusers, name='admusers'),
    path('admproducts/', views.admproducts, name='admproducts'),
    path('admcategories/', views.admcategories, name='admproducts'),
    path('admorders/', views.admorders, name='admorders'),    
    path('admreturns/', views.admreturns, name='admreturns'),
    path('admcoupons/', views.admcoupons, name='admcoupons'),
    path('admbanners/', views.admbanners, name='admbanners'),


]
