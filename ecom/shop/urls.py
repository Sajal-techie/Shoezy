from django.urls import path

from . import views
urlpatterns = [
    path('shop/', views.shop, name='shop' ),
    path('singleproduct/<str:id>/', views.singleproduct, name='singleproduct'),
    path('seachitems/', views.seachitems, name='seachitems'),
  
]
